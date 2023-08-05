import {
    ADD_STORE_APPS,
    DELETE_STORE_APPS,
    SET_STORE_APPS,
    SET_STORE_TOTAL_COUNT,
    STORE_APPS_LOADING,
    UPDATE_STORE_APP,
} from './constants'
export function addStoreApps( apps ) {
    return {
        type: ADD_STORE_APPS,
        payload: apps
    }
}
export function updateStoreApp( app ) {
    return {
        type: UPDATE_STORE_APP,
        payload: app
    }
}
export function deleteStoreApps( appIDs ) {
    return {
        type: DELETE_STORE_APPS,
        payload: appIDs
    }
}
export function setStoreApps( apps ) {
    return {
        type: SET_STORE_APPS,
        payload: apps
    }
}
export function storeAppsLoading( loading ) {
    return {
        type: STORE_APPS_LOADING,
        payload: loading
    }
}
export function storeAppsTotalCount( count ) {
    return {
        type: SET_STORE_TOTAL_COUNT,
        payload: count
    }
}
