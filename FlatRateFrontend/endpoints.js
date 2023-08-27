// this is where we define
// our urls to communicate with the backend

const BASE = "http://10.89.211.86:8000/flatrate"

export default {
    registerPoint:      BASE + "/api-post-new-user/",
    loginPoint:         BASE + "/api-try-login/",
    getFlatmates:       BASE + "/api-get-flatmates/",
    getTallies:         BASE + "/api-get-tallies/",
    //getInterests:       BASE + "/fetch/api-fetch-interests",
    //saveInterests:      BASE + "/push/api-set-user-interests/",
    //getUserInterests:   BASE + "/fetch/api-fetch-user-interests",
    //changePassword:     BASE + "/auth/api-change-password/",
    //availableEvents:    BASE + "/fetch/api-fetch-available-events",
    //attendingEvents:    BASE + "/fetch/api-fetch-attending-events",
    //eventSignOn:        BASE + "/push/api-push-event-sign-on/",
    //getContacts:        BASE + "/fetch/api-fetch-contacts",
    //sendFriendRequest:  BASE + "/push/api-push-pending-contact/",
    //acceptFriendRequest:BASE + "/push/api-push-confirm-contact/",
    //getMessages:        BASE + "/fetch/api-fetch-ordered-messages",
    //sendMessage:        BASE + "/push/api-push-new-message/",
    //getNotifications:   BASE + "/fetch/api-fetch-notifications",
    //specificEvent:      BASE + "/fetch/api-fetch-event-info",
    //isAttending:        BASE + "/fetch/api-fetch-attend-status",
    //transportRecs:      BASE + "/fetc/api-fetch-transport-recommendations"
}