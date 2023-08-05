import {
    SET_ACTIVE_PAGE,
    SET_ITEMS_PER_PAGE,
    SET_SEARCH_TEXT,
    SET_SORT_BY,
    SET_SORT_TYPE
} from './constants'
export function setSortBy( attributeName ) {
    return {
        type: SET_SORT_BY,
        payload: attributeName
    }
}
export function setSearchText( txt ) {
    return {
        type: SET_SEARCH_TEXT,
        payload: txt
    }
}
export function setActivePage( pageNumber ) {
    return {
        type: SET_ACTIVE_PAGE,
        payload: pageNumber
    }
}
export function setItemsPerPage( count ) {
    return {
        type: SET_ITEMS_PER_PAGE,
        payload: count
    }
}
export function setSortType( type ) {
    return {
        type: SET_SORT_TYPE,
        payload: type
    }
}
