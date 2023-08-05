import {
    APP_STORES_LOADING,
    SELECT_APP_STORE,
    SET_APP_STORES
} from './constants'
export function setAppStores( stores ) {
    return {
        type: SET_APP_STORES,
        payload: stores
    }
}
export function selectAppStore( StoreID ) {
    return {
        type: SELECT_APP_STORE,
        payload: StoreID
    }
}
export function appStoresLoading( loading ) {
    return {
        type: APP_STORES_LOADING,
        payload: loading
    }
}
