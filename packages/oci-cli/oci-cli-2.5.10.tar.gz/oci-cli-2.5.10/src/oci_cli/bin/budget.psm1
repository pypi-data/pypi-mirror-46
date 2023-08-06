function GetOciTopLevelCommand_budget() {
    return 'budget'
}

function GetOciSubcommands_budget() {
    $ociSubcommands = @{
        'budget' = 'alert-rule budget'
        'budget alert-rule' = 'create delete get list update'
        'budget budget' = 'create delete get list update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_budget() {
    $ociCommandsToLongParams = @{
        'budget alert-rule create' = 'budget-id defined-tags description display-name freeform-tags from-json help max-wait-seconds message recipients threshold threshold-type type wait-for-state wait-interval-seconds'
        'budget alert-rule delete' = 'alert-rule-id budget-id force from-json help if-match'
        'budget alert-rule get' = 'alert-rule-id budget-id from-json help'
        'budget alert-rule list' = 'all budget-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'budget alert-rule update' = 'alert-rule-id budget-id defined-tags description display-name force freeform-tags from-json help if-match max-wait-seconds message recipients threshold threshold-type type wait-for-state wait-interval-seconds'
        'budget budget create' = 'amount compartment-id defined-tags description display-name freeform-tags from-json help max-wait-seconds reset-period target-compartment-id wait-for-state wait-interval-seconds'
        'budget budget delete' = 'budget-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'budget budget get' = 'budget-id from-json help'
        'budget budget list' = 'all compartment-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'budget budget update' = 'amount budget-id defined-tags description display-name force freeform-tags from-json help if-match max-wait-seconds reset-period wait-for-state wait-interval-seconds'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_budget() {
    $ociCommandsToShortParams = @{
        'budget alert-rule create' = '? h'
        'budget alert-rule delete' = '? h'
        'budget alert-rule get' = '? h'
        'budget alert-rule list' = '? h'
        'budget alert-rule update' = '? h'
        'budget budget create' = '? c h'
        'budget budget delete' = '? h'
        'budget budget get' = '? h'
        'budget budget list' = '? c h'
        'budget budget update' = '? h'
    }
    return $ociCommandsToShortParams
}