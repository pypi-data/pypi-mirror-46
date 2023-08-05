import {
    ADD_INSTALLED_APPS,
    DELETE_INSTALLED_APPS,
    INSTALLED_APPS_LOADING,
    SET_ACTION_IN_PROGRESS,
    SET_APPS_TOTAL_COUNT,
    SET_INSTALLED_APPS,
    UPDATE_INSTALLED_APP,
} from './constants'
export function addApps( apps ) {
    return {
        type: ADD_INSTALLED_APPS,
        payload: apps
    }
}
export function updateInstalledApp( app ) {
    return {
        type: UPDATE_INSTALLED_APP,
        payload: app
    }
}
export function actionInProgress( loading ) {
    return {
        type: SET_ACTION_IN_PROGRESS,
        payload: loading
    }
}
export function deleteInstalledApps( appIDs ) {
    return {
        type: DELETE_INSTALLED_APPS,
        payload: appIDs
    }
}
export function setInstalledApps( apps ) {
    return {
        type: SET_INSTALLED_APPS,
        payload: apps
    }
}
export function installedAppsLoading( loading ) {
    return {
        type: INSTALLED_APPS_LOADING,
        payload: loading
    }
}
export function installedAppsTotalCount( count ) {
    return {
        type: SET_APPS_TOTAL_COUNT,
        payload: count
    }
}
