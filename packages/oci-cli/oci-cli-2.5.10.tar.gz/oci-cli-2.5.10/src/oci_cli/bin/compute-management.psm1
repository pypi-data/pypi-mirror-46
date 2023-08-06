function GetOciTopLevelCommand_compute_management() {
    return 'compute-management'
}

function GetOciSubcommands_compute_management() {
    $ociSubcommands = @{
        'compute-management' = 'instance-configuration instance-pool'
        'compute-management instance-configuration' = 'create delete get launch-compute-instance list update'
        'compute-management instance-pool' = 'attach-lb create detach-lb get list list-instances reset softreset start stop terminate update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_compute_management() {
    $ociCommandsToLongParams = @{
        'compute-management instance-configuration create' = 'compartment-id defined-tags display-name freeform-tags from-json help instance-details'
        'compute-management instance-configuration delete' = 'force from-json help if-match instance-configuration-id'
        'compute-management instance-configuration get' = 'from-json help instance-configuration-id'
        'compute-management instance-configuration launch-compute-instance' = 'block-volumes from-json help instance-configuration-id launch-details secondary-vnics'
        'compute-management instance-configuration list' = 'all compartment-id from-json help limit page page-size sort-by sort-order'
        'compute-management instance-configuration update' = 'defined-tags display-name force freeform-tags from-json help if-match instance-configuration-id'
        'compute-management instance-pool attach-lb' = 'backend-set-name from-json help if-match instance-pool-id load-balancer-id max-wait-seconds port vnic-selection wait-for-state wait-interval-seconds'
        'compute-management instance-pool create' = 'compartment-id defined-tags display-name freeform-tags from-json help instance-configuration-id load-balancers max-wait-seconds placement-configurations size wait-for-state wait-interval-seconds'
        'compute-management instance-pool detach-lb' = 'backend-set-name from-json help if-match instance-pool-id load-balancer-id max-wait-seconds wait-for-state wait-interval-seconds'
        'compute-management instance-pool get' = 'from-json help instance-pool-id'
        'compute-management instance-pool list' = 'all compartment-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'compute-management instance-pool list-instances' = 'all compartment-id display-name from-json help instance-pool-id limit page page-size sort-by sort-order'
        'compute-management instance-pool reset' = 'from-json help if-match instance-pool-id max-wait-seconds wait-for-state wait-interval-seconds'
        'compute-management instance-pool softreset' = 'from-json help if-match instance-pool-id max-wait-seconds wait-for-state wait-interval-seconds'
        'compute-management instance-pool start' = 'from-json help if-match instance-pool-id max-wait-seconds wait-for-state wait-interval-seconds'
        'compute-management instance-pool stop' = 'from-json help if-match instance-pool-id max-wait-seconds wait-for-state wait-interval-seconds'
        'compute-management instance-pool terminate' = 'force from-json help if-match instance-pool-id max-wait-seconds wait-for-state wait-interval-seconds'
        'compute-management instance-pool update' = 'defined-tags display-name force freeform-tags from-json help if-match instance-configuration-id instance-pool-id max-wait-seconds placement-configurations size wait-for-state wait-interval-seconds'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_compute_management() {
    $ociCommandsToShortParams = @{
        'compute-management instance-configuration create' = '? c h'
        'compute-management instance-configuration delete' = '? h'
        'compute-management instance-configuration get' = '? h'
        'compute-management instance-configuration launch-compute-instance' = '? h'
        'compute-management instance-configuration list' = '? c h'
        'compute-management instance-configuration update' = '? h'
        'compute-management instance-pool attach-lb' = '? h'
        'compute-management instance-pool create' = '? c h'
        'compute-management instance-pool detach-lb' = '? h'
        'compute-management instance-pool get' = '? h'
        'compute-management instance-pool list' = '? c h'
        'compute-management instance-pool list-instances' = '? c h'
        'compute-management instance-pool reset' = '? h'
        'compute-management instance-pool softreset' = '? h'
        'compute-management instance-pool start' = '? h'
        'compute-management instance-pool stop' = '? h'
        'compute-management instance-pool terminate' = '? h'
        'compute-management instance-pool update' = '? h'
    }
    return $ociCommandsToShortParams
}