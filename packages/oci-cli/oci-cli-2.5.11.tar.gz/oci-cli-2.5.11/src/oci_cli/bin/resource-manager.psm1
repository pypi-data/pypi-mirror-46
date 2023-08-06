function GetOciTopLevelCommand_resource_manager() {
    return 'resource-manager'
}

function GetOciSubcommands_resource_manager() {
    $ociSubcommands = @{
        'resource-manager' = 'job stack'
        'resource-manager job' = 'cancel create get get-job-logs get-job-logs-content get-job-tf-config get-job-tf-state list update'
        'resource-manager stack' = 'create delete get get-stack-tf-config list update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_resource_manager() {
    $ociCommandsToLongParams = @{
        'resource-manager job cancel' = 'force from-json help if-match job-id max-wait-seconds wait-for-state wait-interval-seconds'
        'resource-manager job create' = 'apply-job-plan-resolution defined-tags display-name freeform-tags from-json help max-wait-seconds operation stack-id wait-for-state wait-interval-seconds'
        'resource-manager job get' = 'from-json help job-id'
        'resource-manager job get-job-logs' = 'from-json help job-id level-greater-than-or-equal-to limit page sort-order timestamp-greater-than-or-equal-to timestamp-less-than-or-equal-to type'
        'resource-manager job get-job-logs-content' = 'from-json help job-id'
        'resource-manager job get-job-tf-config' = 'file from-json help job-id'
        'resource-manager job get-job-tf-state' = 'file from-json help job-id'
        'resource-manager job list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order stack-id'
        'resource-manager job update' = 'defined-tags display-name force freeform-tags from-json help if-match job-id max-wait-seconds wait-for-state wait-interval-seconds'
        'resource-manager stack create' = 'compartment-id config-source defined-tags description display-name freeform-tags from-json help max-wait-seconds variables wait-for-state wait-interval-seconds working-directory'
        'resource-manager stack delete' = 'force from-json help if-match max-wait-seconds stack-id wait-for-state wait-interval-seconds'
        'resource-manager stack get' = 'from-json help stack-id'
        'resource-manager stack get-stack-tf-config' = 'file from-json help stack-id'
        'resource-manager stack list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order'
        'resource-manager stack update' = 'config-source defined-tags description display-name force freeform-tags from-json help if-match max-wait-seconds stack-id variables wait-for-state wait-interval-seconds working-directory'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_resource_manager() {
    $ociCommandsToShortParams = @{
        'resource-manager job cancel' = '? h'
        'resource-manager job create' = '? h'
        'resource-manager job get' = '? h'
        'resource-manager job get-job-logs' = '? h'
        'resource-manager job get-job-logs-content' = '? h'
        'resource-manager job get-job-tf-config' = '? h'
        'resource-manager job get-job-tf-state' = '? h'
        'resource-manager job list' = '? c h'
        'resource-manager job update' = '? h'
        'resource-manager stack create' = '? c h'
        'resource-manager stack delete' = '? h'
        'resource-manager stack get' = '? h'
        'resource-manager stack get-stack-tf-config' = '? h'
        'resource-manager stack list' = '? c h'
        'resource-manager stack update' = '? h'
    }
    return $ociCommandsToShortParams
}