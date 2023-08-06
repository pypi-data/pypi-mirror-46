import base64

import flask
from marshmallow import ValidationError
import sqlalchemy as sa

from . import meta
from .exceptions import ApiError
from .utils import if_none, iter_validation_errors

# -----------------------------------------------------------------------------


class PaginationBase:
    def get_page(self, query, view):
        raise NotImplementedError()

    def get_item_meta(self, item, view):
        return None


# -----------------------------------------------------------------------------


class LimitPaginationBase(PaginationBase):
    def get_page(self, query, view):
        limit = self.get_limit()
        if limit is not None:
            query = query.limit(limit + 1)

        items = query.all()

        if limit is not None and len(items) > limit:
            has_next_page = True
            items = items[:limit]
        else:
            has_next_page = False

        meta.update_response_meta({'has_next_page': has_next_page})
        return items

    def get_limit(self):
        raise NotImplementedError()


class MaxLimitPagination(LimitPaginationBase):
    def __init__(self, max_limit):
        self._max_limit = max_limit

    def get_limit(self):
        return self._max_limit


class LimitPagination(LimitPaginationBase):
    limit_arg = 'limit'

    def __init__(self, default_limit=None, max_limit=None):
        self._default_limit = if_none(default_limit, max_limit)
        self._max_limit = max_limit

        if self._max_limit is not None:
            assert self._default_limit <= self._max_limit, (
                "default limit exceeds max limit"
            )

    def get_limit(self):
        limit = flask.request.args.get(self.limit_arg)
        try:
            return self.parse_limit(limit)
        except ApiError as e:
            raise e.update({'source': {'parameter': self.limit_arg}})

    def parse_limit(self, limit):
        if limit is None:
            return self._default_limit

        try:
            limit = int(limit)
        except ValueError:
            raise ApiError(400, {'code': 'invalid_limit'})
        if limit < 0:
            raise ApiError(400, {'code': 'invalid_limit'})

        if self._max_limit is not None:
            limit = min(limit, self._max_limit)

        return limit


class LimitOffsetPagination(LimitPagination):
    offset_arg = 'offset'

    def get_page(self, query, view):
        offset = self.get_offset()
        query = query.offset(offset)
        return super().get_page(query, view)

    def get_offset(self):
        offset = flask.request.args.get(self.offset_arg)
        try:
            return self.parse_offset(offset)
        except ApiError as e:
            raise e.update({'source': {'parameter': self.offset_arg}})

    def parse_offset(self, offset):
        if offset is None:
            return 0

        try:
            offset = int(offset)
        except ValueError:
            raise ApiError(400, {'code': 'invalid_offset'})
        if offset < 0:
            raise ApiError(400, {'code': 'invalid_offset'})

        return offset


class PagePagination(LimitOffsetPagination):
    page_arg = 'page'

    def __init__(self, page_size):
        super().__init__()
        self._page_size = page_size

    def get_offset(self):
        return self.get_request_page() * self._page_size

    def get_request_page(self):
        page = flask.request.args.get(self.page_arg)
        try:
            return self.parse_page(page)
        except ApiError as e:
            raise e.update({'source': {'parameter': self.page_arg}})

    def parse_page(self, page):
        if page is None:
            return 0

        try:
            page = int(page)
        except ValueError:
            raise ApiError(400, {'code': 'invalid_page'})
        if page < 0:
            raise ApiError(400, {'code': 'invalid_page'})

        return page

    def get_limit(self):
        return self._page_size


# -----------------------------------------------------------------------------


class CursorPaginationBase(LimitPagination):
    cursor_arg = 'cursor'

    def ensure_query_sorting(self, query, view):
        sorting_field_orderings, missing_field_orderings = (
            self.get_sorting_and_missing_field_orderings(view)
        )

        query = view.sorting.sort_query_by_fields(
            query,
            view,
            missing_field_orderings,
        )
        field_orderings = sorting_field_orderings + missing_field_orderings

        return query, field_orderings

    def get_field_orderings(self, view):
        sorting_field_orderings, missing_field_orderings = (
            self.get_sorting_and_missing_field_orderings(view)
        )
        return sorting_field_orderings + missing_field_orderings

    def get_sorting_and_missing_field_orderings(self, view):
        sorting = view.sorting
        assert sorting is not None, (
            "sorting must be defined when using cursor pagination"
        )

        sorting_field_orderings = sorting.get_request_field_orderings(view)

        sorting_ordering_fields = frozenset(
            field_name for field_name, _ in sorting_field_orderings
        )

        # For convenience, use the ascending setting on the last explicit
        # ordering when possible, such that reversing the sort will reverse
        # the IDs as well.
        if sorting_field_orderings:
            last_field_asc = sorting_field_orderings[-1][1]
        else:
            last_field_asc = True

        missing_field_orderings = tuple(
            (id_field, last_field_asc) for id_field in view.id_fields
            if id_field not in sorting_ordering_fields
        )

        return sorting_field_orderings, missing_field_orderings

    def get_request_cursor(self, view, field_orderings):
        cursor = flask.request.args.get(self.cursor_arg)
        if not cursor:
            return None

        try:
            return self.parse_cursor(cursor, view, field_orderings)
        except ApiError as e:
            raise e.update({'source': {'parameter': self.cursor_arg}})

    def parse_cursor(self, cursor, view, field_orderings):
        cursor = self.decode_cursor(cursor)

        if len(cursor) != len(field_orderings):
            raise ApiError(400, {'code': 'invalid_cursor.length'})

        deserializer = view.deserializer
        column_fields = (
            deserializer.fields[field_name]
            for field_name, _ in field_orderings
        )

        try:
            cursor = tuple(
                field.deserialize(value)
                for field, value in zip(column_fields, cursor)
            )
        except ValidationError as e:
            raise ApiError(400, *(
                self.format_validation_error(message)
                for message, path in iter_validation_errors(e.messages)
            ))

        return cursor

    def decode_cursor(self, cursor):
        try:
            cursor = cursor.split('.')
            cursor = tuple(self.decode_value(value) for value in cursor)
        except (TypeError, ValueError):
            raise ApiError(400, {'code': 'invalid_cursor.encoding'})

        return cursor

    def decode_value(self, value):
        value = value.encode('ascii')
        value += (3 - ((len(value) + 3) % 4)) * b'='  # Add back padding.
        value = base64.urlsafe_b64decode(value)
        return value.decode()

    def format_validation_error(self, message):
        return {
            'code': 'invalid_cursor',
            'detail': message,
        }

    def get_filter(self, view, field_orderings, cursor):
        sorting = view.sorting

        column_cursors = tuple(
            (sorting.get_column(view, field_name), asc, value)
            for (field_name, asc), value in zip(field_orderings, cursor)
        )

        return sa.or_(
            self.get_filter_clause(column_cursors[:i + 1])
            for i in range(len(column_cursors))
        )

    def get_filter_clause(self, column_cursors):
        previous_clauses = sa.and_(
            column == value for column, _, value in column_cursors[:-1]
        )

        column, asc, value = column_cursors[-1]
        if asc:
            current_clause = column > value
        else:
            current_clause = column < value

        return sa.and_(previous_clauses, current_clause)

    def make_cursors(self, items, view, field_orderings):
        column_fields = self.get_column_fields(view, field_orderings)
        return tuple(
            self.render_cursor(item, column_fields) for item in items
        )

    def make_cursor(self, item, view, field_orderings):
        column_fields = self.get_column_fields(view, field_orderings)
        return self.render_cursor(item, column_fields)

    def get_column_fields(self, view, field_orderings):
        serializer = view.serializer
        return tuple(
            serializer.fields[field_name]
            for field_name, _ in field_orderings
        )

    def render_cursor(self, item, column_fields):
        cursor = tuple(
            field._serialize(getattr(item, field.name), field.name, item)
            for field in column_fields
        )

        return self.encode_cursor(cursor)

    def encode_cursor(self, cursor):
        return '.'.join(self.encode_value(value) for value in cursor)

    def encode_value(self, value):
        value = str(value)
        value = value.encode()
        value = base64.urlsafe_b64encode(value)
        value = value.rstrip(b'=')  # Strip padding.
        return value.decode('ascii')


class RelayCursorPagination(CursorPaginationBase):
    def get_page(self, query, view):
        query, field_orderings = self.ensure_query_sorting(query, view)

        cursor_in = self.get_request_cursor(view, field_orderings)
        if cursor_in is not None:
            query = query.filter(
                self.get_filter(view, field_orderings, cursor_in),
            )

        items = super().get_page(query, view)

        # Relay expects a cursor for each item.
        cursors_out = self.make_cursors(items, view, field_orderings)
        meta.update_response_meta({'cursors': cursors_out})

        return items

    def get_item_meta(self, item, view):
        field_orderings = self.get_field_orderings(view)

        cursor = self.make_cursor(item, view, field_orderings)
        return {'cursor': cursor}
