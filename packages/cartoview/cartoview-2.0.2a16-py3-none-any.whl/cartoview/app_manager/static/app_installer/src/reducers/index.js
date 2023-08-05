// import {
//     token,
//     urls,
//     username
// } from './other'

import {
    appErrors,
} from './errors'
import {
    appFilters,
} from './filter'
import {
    appStores,
} from './stores'
import {
    apps,
} from './apps'
import { combineReducers } from 'redux'
export default combineReducers( {
    apps,
    appStores,
    appFilters,
    appErrors,
    // urls,
    // username,
    // token,
} )
