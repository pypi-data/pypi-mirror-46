function GetOciTopLevelCommand_kms() {
    return 'kms'
}

function GetOciSubcommands_kms() {
    $ociSubcommands = @{
        'kms' = 'crypto management'
        'kms crypto' = 'decrypt encrypt generate-data-encryption-key'
        'kms management' = 'key key-version vault'
        'kms management key' = 'create disable enable get list update'
        'kms management key-version' = 'create get list'
        'kms management vault' = 'cancel-deletion create get list schedule-deletion update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_kms() {
    $ociCommandsToLongParams = @{
        'kms crypto decrypt' = 'associated-data ciphertext from-json help key-id logging-context'
        'kms crypto encrypt' = 'associated-data from-json help key-id logging-context plaintext'
        'kms crypto generate-data-encryption-key' = 'associated-data from-json help include-plaintext-key key-id key-shape logging-context'
        'kms management key create' = 'compartment-id defined-tags display-name freeform-tags from-json help key-shape max-wait-seconds wait-for-state wait-interval-seconds'
        'kms management key disable' = 'from-json help if-match key-id max-wait-seconds wait-for-state wait-interval-seconds'
        'kms management key enable' = 'from-json help if-match key-id max-wait-seconds wait-for-state wait-interval-seconds'
        'kms management key get' = 'from-json help key-id'
        'kms management key list' = 'all compartment-id from-json help limit page page-size sort-by sort-order'
        'kms management key update' = 'defined-tags display-name force freeform-tags from-json help if-match key-id max-wait-seconds wait-for-state wait-interval-seconds'
        'kms management key-version create' = 'from-json help key-id'
        'kms management key-version get' = 'from-json help key-id key-version-id'
        'kms management key-version list' = 'all from-json help key-id limit page page-size sort-by sort-order'
        'kms management vault cancel-deletion' = 'from-json help if-match max-wait-seconds vault-id wait-for-state wait-interval-seconds'
        'kms management vault create' = 'compartment-id defined-tags display-name freeform-tags from-json help max-wait-seconds vault-type wait-for-state wait-interval-seconds'
        'kms management vault get' = 'from-json help vault-id'
        'kms management vault list' = 'all compartment-id from-json help limit page page-size sort-by sort-order'
        'kms management vault schedule-deletion' = 'from-json help if-match max-wait-seconds time-of-deletion vault-id wait-for-state wait-interval-seconds'
        'kms management vault update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds vault-id wait-for-state wait-interval-seconds'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_kms() {
    $ociCommandsToShortParams = @{
        'kms crypto decrypt' = '? h'
        'kms crypto encrypt' = '? h'
        'kms crypto generate-data-encryption-key' = '? h'
        'kms management key create' = '? c h'
        'kms management key disable' = '? h'
        'kms management key enable' = '? h'
        'kms management key get' = '? h'
        'kms management key list' = '? c h'
        'kms management key update' = '? h'
        'kms management key-version create' = '? h'
        'kms management key-version get' = '? h'
        'kms management key-version list' = '? h'
        'kms management vault cancel-deletion' = '? h'
        'kms management vault create' = '? c h'
        'kms management vault get' = '? h'
        'kms management vault list' = '? c h'
        'kms management vault schedule-deletion' = '? h'
        'kms management vault update' = '? h'
    }
    return $ociCommandsToShortParams
}