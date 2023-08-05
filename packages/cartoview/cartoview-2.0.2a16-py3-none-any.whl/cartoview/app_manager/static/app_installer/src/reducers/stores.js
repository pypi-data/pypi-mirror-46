import {
    APP_STORES_LOADING,
    SELECT_APP_STORE,
    SET_APP_STORES,
} from '../actions/constants'
let appStoresInitailState = {
    stores: [],
    selectedStoreID: null,
    loading: true
}
export function appStores( state = appStoresInitailState, action ) {
    switch ( action.type ) {
    case SELECT_APP_STORE:
        return { ...state, selectedStoreID: action.payload }
    case SET_APP_STORES:
        return { ...state, stores: action.payload }
    case APP_STORES_LOADING:
        return { ...state, loading: action.payload }
    default:
        return state
    }
}
