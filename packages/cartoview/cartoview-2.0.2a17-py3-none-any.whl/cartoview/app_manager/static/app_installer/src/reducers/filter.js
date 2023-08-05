import {
    SET_ACTIVE_PAGE,
    SET_ITEMS_PER_PAGE,
    SET_SEARCH_TEXT,
    SET_SORT_BY,
    SET_SORT_TYPE
} from '../actions/constants'
let appConfig = {
    searchText: '',
    sortBy: 'title',
    activePage: 1,
    itemsPerPage: 9,
    sortType: 'asc'
}
export function appFilters( state = appConfig, action ) {
    switch ( action.type ) {
    case SET_SEARCH_TEXT:
        return { ...state, searchText: action.payload }
    case SET_SORT_BY:
        return { ...state, sortBy: action.payload }
    case SET_ACTIVE_PAGE:
        return { ...state, activePage: action.payload }
    case SET_ITEMS_PER_PAGE:
        return { ...state, itemsPerPage: action.payload }
    case SET_SORT_TYPE:
        return { ...state, sortType: action.payload }
    default:
        return state
    }
}
