function GetOciTopLevelCommand_announcements_service() {
    return 'announcements-service'
}

function GetOciSubcommands_announcements_service() {
    $ociSubcommands = @{
        'announcements-service' = 'announcement announcement-user-status announcement-user-status-details announcements-collection'
        'announcements-service announcement' = 'get'
        'announcements-service announcement-user-status' = 'update'
        'announcements-service announcement-user-status-details' = 'get-announcement-user-status'
        'announcements-service announcements-collection' = 'list-announcements'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_announcements_service() {
    $ociCommandsToLongParams = @{
        'announcements-service announcement get' = 'announcement-id from-json help'
        'announcements-service announcement-user-status update' = 'announcement-id from-json help if-match time-acknowledged user-id user-status-announcement-id'
        'announcements-service announcement-user-status-details get-announcement-user-status' = 'announcement-id from-json help'
        'announcements-service announcements-collection list-announcements' = 'all announcement-type compartment-id from-json help is-banner lifecycle-state limit page page-size sort-by sort-order time-one-earliest-time time-one-latest-time'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_announcements_service() {
    $ociCommandsToShortParams = @{
        'announcements-service announcement get' = '? h'
        'announcements-service announcement-user-status update' = '? h'
        'announcements-service announcement-user-status-details get-announcement-user-status' = '? h'
        'announcements-service announcements-collection list-announcements' = '? c h'
    }
    return $ociCommandsToShortParams
}