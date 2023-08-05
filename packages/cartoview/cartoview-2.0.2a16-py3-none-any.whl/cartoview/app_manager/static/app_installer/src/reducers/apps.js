import {
    ADD_INSTALLED_APPS,
    ADD_STORE_APPS,
    DELETE_INSTALLED_APPS,
    DELETE_STORE_APPS,
    INSTALLED_APPS_LOADING,
    SET_ACTION_IN_PROGRESS,
    SET_APPS_TOTAL_COUNT,
    SET_INSTALLED_APPS,
    SET_STORE_APPS,
    SET_STORE_TOTAL_COUNT,
    STORE_APPS_LOADING,
    UPDATE_INSTALLED_APP,
    UPDATE_STORE_APP
} from '../actions/constants'
let appsInitailState = {
    installed: [],
    storeApps: [],
    installedAppsLoading: true,
    storeAppsLoading: true,
    installedCount: 0,
    storeCount: 0,
    inProgress: false
}
export function apps( state = appsInitailState, action ) {
    switch ( action.type ) {
    case ADD_INSTALLED_APPS:
        return { ...state, installed: [ ...state.installed, ...action.payload ] }
    case ADD_STORE_APPS:
        return { ...state, storeApps: [ ...state.storeApps, ...action.payload ] }
    case DELETE_INSTALLED_APPS:        
        return {
            ...state,
            installed: state.installed.map( app => !action.payload.includes(
                app.id ) )
        }
    case DELETE_STORE_APPS:
        return {
            ...state,
            storeApps: state.storeApps.map( app => !action.payload.includes(
                app.id ) )
        }
    case SET_INSTALLED_APPS:
        return { ...state, installed: action.payload }
    case SET_STORE_APPS:
        return { ...state, storeApps: action.payload }
    case UPDATE_INSTALLED_APP:
        return {
            ...state,
            installed: state.installed.map( app => {
                if ( app.id === action.payload.id ) {
                    return { ...app, ...action.payload }
                }
                return app
            } )
        }
    case UPDATE_STORE_APP:
        return {
            ...state,
            storeApps: state.storeApps.map( storeApp => {
                if ( storeApp.id === action.payload.id ) {
                    return { ...storeApp, ...action.payload }
                }
                return storeApp
            } )
        }
    case INSTALLED_APPS_LOADING:
        return { ...state, installedAppsLoading: action.payload }
    case STORE_APPS_LOADING:
        return { ...state, storeAppsLoading: action.payload }
    case SET_APPS_TOTAL_COUNT:
        return { ...state, installedCount: action.payload }
    case SET_STORE_TOTAL_COUNT:
        return { ...state, storeCount: action.payload }
    case SET_ACTION_IN_PROGRESS:
        return { ...state, inProgress: action.payload }
    default:
        return state
    }
}
