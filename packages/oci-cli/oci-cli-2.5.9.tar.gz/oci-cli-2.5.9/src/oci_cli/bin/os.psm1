function GetOciTopLevelCommand_os() {
    return 'os'
}

function GetOciSubcommands_os() {
    $ociSubcommands = @{
        'os' = 'bucket multipart ns object object-lifecycle-policy preauth-request work-request work-request-error work-request-log-entry'
        'os bucket' = 'create delete get list update'
        'os multipart' = 'abort list'
        'os ns' = 'get get-metadata update-metadata'
        'os object' = 'bulk-delete bulk-download bulk-upload copy delete get head list put rename restore restore-status resume-put'
        'os object-lifecycle-policy' = 'delete get put'
        'os preauth-request' = 'create delete get list'
        'os work-request' = 'cancel get list'
        'os work-request-error' = 'list'
        'os work-request-log-entry' = 'list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_os() {
    $ociCommandsToLongParams = @{
        'os bucket create' = 'compartment-id defined-tags freeform-tags from-json help kms-key-id metadata name namespace namespace-name public-access-type storage-tier'
        'os bucket delete' = 'bucket-name force from-json help if-match name namespace namespace-name'
        'os bucket get' = 'bucket-name fields from-json help if-match if-none-match name namespace namespace-name'
        'os bucket list' = 'all compartment-id fields from-json help limit namespace namespace-name page page-size'
        'os bucket update' = 'bucket-name compartment-id defined-tags freeform-tags from-json help if-match kms-key-id metadata name namespace namespace-name public-access-type'
        'os multipart abort' = 'bucket-name force from-json help namespace namespace-name object-name upload-id'
        'os multipart list' = 'all bucket-name from-json help limit namespace namespace-name page page-size'
        'os ns get' = 'from-json help'
        'os ns get-metadata' = 'from-json help namespace namespace-name'
        'os ns update-metadata' = 'default-s3-compartment-id default-swift-compartment-id from-json help namespace namespace-name'
        'os object bulk-delete' = 'bucket-name delimiter dry-run exclude force from-json help include namespace namespace-name parallel-operations-count prefix'
        'os object bulk-download' = 'bucket-name delimiter download-dir exclude from-json help include multipart-download-threshold namespace namespace-name no-overwrite overwrite parallel-operations-count part-size prefix'
        'os object bulk-upload' = 'bucket-name content-encoding content-language content-type disable-parallel-uploads exclude from-json help include metadata namespace namespace-name no-multipart no-overwrite object-prefix overwrite parallel-upload-count part-size src-dir'
        'os object copy' = 'bucket-name destination-bucket destination-namespace destination-object-if-match-e-tag destination-object-if-none-match-e-tag destination-object-metadata destination-object-name destination-region from-json help max-wait-seconds namespace namespace-name source-object-if-match-e-tag source-object-name wait-for-state wait-interval-seconds'
        'os object delete' = 'bucket-name force from-json help if-match name namespace namespace-name object-name'
        'os object get' = 'bucket-name file from-json help if-match if-none-match multipart-download-threshold name namespace namespace-name parallel-download-count part-size range'
        'os object head' = 'bucket-name from-json help if-match if-none-match name namespace namespace-name'
        'os object list' = 'all bucket-name delimiter end fields from-json help limit namespace namespace-name page-size prefix start'
        'os object put' = 'bucket-name content-encoding content-language content-md5 content-type disable-parallel-uploads file force from-json help if-match metadata name namespace namespace-name no-multipart no-overwrite parallel-upload-count part-size'
        'os object rename' = 'bucket bucket-name from-json help name namespace namespace-name new-if-match new-if-none-match new-name new-obj-if-match-e-tag new-obj-if-none-match-e-tag source-name src-if-match src-obj-if-match-e-tag'
        'os object restore' = 'bucket bucket-name from-json help hours name namespace namespace-name'
        'os object restore-status' = 'bucket-name from-json help name namespace namespace-name'
        'os object resume-put' = 'bucket-name disable-parallel-uploads file from-json help name namespace namespace-name parallel-upload-count part-size upload-id'
        'os object-lifecycle-policy delete' = 'bucket-name force from-json help if-match namespace namespace-name'
        'os object-lifecycle-policy get' = 'bucket-name from-json help namespace namespace-name'
        'os object-lifecycle-policy put' = 'bucket-name force from-json help if-match if-none-match items namespace namespace-name'
        'os preauth-request create' = 'access-type bucket-name from-json help name namespace namespace-name object-name time-expires'
        'os preauth-request delete' = 'bucket-name force from-json help namespace namespace-name par-id'
        'os preauth-request get' = 'bucket-name from-json help namespace namespace-name par-id'
        'os preauth-request list' = 'all bucket-name from-json help limit namespace namespace-name object-name-prefix page page-size'
        'os work-request cancel' = 'force from-json help work-request-id'
        'os work-request get' = 'from-json help work-request-id'
        'os work-request list' = 'all compartment-id from-json help limit page page-size'
        'os work-request-error list' = 'all from-json help limit page page-size work-request-id'
        'os work-request-log-entry list' = 'all from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_os() {
    $ociCommandsToShortParams = @{
        'os bucket create' = '? c h ns'
        'os bucket delete' = '? bn h ns'
        'os bucket get' = '? bn h ns'
        'os bucket list' = '? c h ns'
        'os bucket update' = '? bn c h ns'
        'os multipart abort' = '? bn h ns on'
        'os multipart list' = '? bn h ns'
        'os ns get' = '? h'
        'os ns get-metadata' = '? h ns'
        'os ns update-metadata' = '? h ns'
        'os object bulk-delete' = '? bn h ns'
        'os object bulk-download' = '? bn h ns'
        'os object bulk-upload' = '? bn h ns'
        'os object copy' = '? bn h ns'
        'os object delete' = '? bn h ns'
        'os object get' = '? bn h ns'
        'os object head' = '? bn h ns'
        'os object list' = '? bn h ns'
        'os object put' = '? bn h ns'
        'os object rename' = '? bn h ns'
        'os object restore' = '? bn h ns'
        'os object restore-status' = '? bn h ns'
        'os object resume-put' = '? bn h ns'
        'os object-lifecycle-policy delete' = '? bn h ns'
        'os object-lifecycle-policy get' = '? bn h ns'
        'os object-lifecycle-policy put' = '? bn h ns'
        'os preauth-request create' = '? bn h ns on'
        'os preauth-request delete' = '? bn h ns'
        'os preauth-request get' = '? bn h ns'
        'os preauth-request list' = '? bn h ns'
        'os work-request cancel' = '? h'
        'os work-request get' = '? h'
        'os work-request list' = '? c h'
        'os work-request-error list' = '? h'
        'os work-request-log-entry list' = '? h'
    }
    return $ociCommandsToShortParams
}