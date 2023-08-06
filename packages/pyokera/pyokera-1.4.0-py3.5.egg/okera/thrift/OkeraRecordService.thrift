// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

namespace py okera.OkeraRecordService
namespace cpp recordservice
namespace java com.okera.recordservice.ext.thrift

include "RecordService.thrift"

// The supported catalog objects for for which total record count
// can be retrieved. This will be expanded as needed
enum TCatalogObjectType {
  ATTRIBUTE
}

struct TCreateAttributesParams {
  1: required list<RecordService.TAttribute> attributes
  2: required string requesting_user
}

struct TCreateAttributesResult {
  1: required list<RecordService.TAttribute> attributes
}

struct TGetAttributesParams {
  1: required string requesting_user
  2: optional RecordService.TAttribute filter_attribute
  3: optional i32 offset
  4: optional i32 count
}

struct TGetAttributesResult {
  1: required list<RecordService.TAttribute> attributes
}

struct TGetCountParams {
  1: required string requesting_user
  2: required TCatalogObjectType object_type
}

struct TGetCountResult {
  1: required i32 total_count
  2: required bool is_total_count_estimated;
}

struct TAssignAttributesParams {
  1: required string requesting_user
  2: required list<RecordService.TAttributeValue> mappings
}

struct TAssignAttributesResult {
  1: required list<RecordService.TAttributeValue> mappings
}

struct TUnassignAttributesParams {
  1: required string requesting_user
  2: required list<RecordService.TAttributeValue> mappings
}

struct TGetAttributeNamespacesParams {
  1: required string requesting_user
}

struct TGetAttributeNamespacesResult {
  1: required list<string> namespaces
}

struct TUnassignAttributesResult {
  1: required i32 unassigned_count
}

struct TDeleteAttributesParams {
  1: required string requesting_user
  2: required list<RecordService.TAttribute> attributes
  // By default cascade is true. Meaning all attribute assignments and grants
  // associated to the attribute will be removed. If set to false,
  // only the attributes and assignments will be removed, leaving the grants behind
  3: optional bool cascade
}

struct TDeleteAttributesResult {
  1: required i32 delete_count
  2: required list<RecordService.TAttribute> attributes
}

struct TSetAttributesParams {
  // This user needs both ADD_ATTRIBUTE and REMOVE_ATTRIBUTE privileges
  1: required string requesting_user
  // The TAttributeValues that comprise the new attributes set.
  // The database/table/column fields allow a bulk set.
  2: required list<RecordService.TAttributeValue> mappings
}

struct TSetAttributesResult {
  // The TAttributeValues that were set
  1: required list<RecordService.TAttributeValue> mappings
}

// Requests access permissions for tables
struct TGetAccessPermissionsParams {
  // The users (or groups) to query access permissions for.
  1: required list<string> users_or_groups

  // Database to request permissions on
  2: required string database

  // Filter to apply to tables within the database
  3: optional string filter

  // User making the request, if not set, will use the connected user
  4: optional string requesting_user
}

enum TAccessPermissionLevel {
  ALL,
  CREATE,
  CREATE_AS_OWNER,
  ALTER,
  INSERT,
  SELECT,
  SHOW,
  ADD_ATTRIBUTE,
  REMOVE_ATTRIBUTE,
}

enum TAccessPermissionScope {
  SERVER,
  DATABASE,
  TABLE,
  COLUMN,
}

struct TRoleAttributeExpression {
  1: required string role_name
  2: required string expression
}

struct TAccessPermission {
  // The list of users/groups that have this access.
  1: required list<string> users_or_groups

  // For each user/group, the role that granted them this access. Note that it is
  // possible multiple roles granted them this, this returns just one of them.
  2: required list<string> roles

  3: required TAccessPermissionLevel level
  4: required bool has_grant
  5: required string database
  6: required string table
  7: required TAccessPermissionScope scope

  // The projection that is accessible
  8: optional list<string> projection

  // attribute expression affecting the access permission for the role
  9: optional list<TRoleAttributeExpression> attribute_expression
}

struct TGetAccessPermissionsResult {
  1: required list<TAccessPermission> permissions
  // For every value in users_or_groups from TGetAccessPermissionsParams,
  // a boolean whether it is a user or not
  2: required list<bool> is_user_flags
}

struct TExecDDLParams {
  1: required string ddl

  // User running the request
  2: optional string requesting_user

  // If set, the default db to use when executing the ddl statement. If not
  // set, the default db is 'default'
  3: optional string defaultdb
}

// Result for a DDL statement. Note that none of the fields need to be set for
// DDL that does not return a result (e.g. create table).
struct TExecDDLResult {
  // Set if the result is tabular. col_names is the headers of the table
  // and tabular_result contain the resutls row by row.
  1: optional list<string> col_names
  2: optional list<list<string>> tabular_result

  // Set if the result is not tabular and should just be output in fixed-width font.
  3: optional string formatted_result

  // Warnings generated while processing this request.
  4: optional list<RecordService.TLogMessage> warnings
}

struct TGetRoleProvenanceParams {
  // The user to query role provenance for
  1: optional string user
}

struct TRoleProvenance {
  // The name of the role
  1: required string role
  // The list of groups granting this role
  2: required list<string> provenance
}

struct TGetRoleProvenanceResult {
  // The requesting user
  1: required string user
  // The groups this user belongs to
  2: required list<string> groups
  // The roles and provenance this user belongs to
  3: required list<TRoleProvenance> roles

  // Return a list of groups which have access to datasets where this user is admin.
  4: optional set<string> groups_administered
  // Return a list of databases for which this user is admin on at least one datasets
  5: optional set<string> databases_administered
}

struct TGetAuthenticatedUserResult {
  // Returns the authenticated user name
  1: required string user

  // If set, the credentials used to authenticate this user will expire in
  // this number of milliseconds.
  // If not set, the credentials will not expire.
  2: optional i64 expires_in_ms
}

struct TGetRegisteredObjectsParams {
  1: required string prefix_path
  // The user running the request. Can be unset if this should just be the connected
  // user.
  2: optional string requesting_user

  // If true, also return views that are in the catalog over these paths
  3: optional bool include_views
}

struct TGetRegisteredObjectsResult {
  // The list of objects, as fully qualified names. e.g. 'db' or 'db.table' by path.
  1: required map<string, set<string>> object_names
}

struct TGetDatasetsParams {
  // The user running the request. Can be unset if this should just be the connected
  // user.
  1: optional string requesting_user

  // Returns datasets only in this database
  2: optional list<string> databases

  // If set, only return datasets where the requesting user has these levels of
  // access.
  3: optional list<TAccessPermissionLevel> access_levels

  // If set, only match datasets which contain this string
  4: optional string filter

  // List of fully qualified dataset names to return metadata for. Cannot be used
  // with databases and filter.
  10: optional list<string> dataset_names

  // If true, also return the schema for the dataset
  5: optional bool with_schema

  // If true, only return the names of the datasets, with no other metadata
  11: optional bool names_only

  // If set, return the full details for the first `full_details_count` and just
  // the names for the remainder. Cannot be used with `names_only`. If not set,
  // returns the full details for all returned datasets.
  13: optional i32 full_details_count

  // Attribute key-namespace-value. Cannot be used with 'dataset_names'
  // If set, only datasets which have these attributes will be returned
  14: optional RecordService.TAttributeValue attribute_value

  // If set, the set of groups to return permissions for. This means that for each dataset
  // returned, the server will return the groups in this list that have some access to
  // those datasets.
  // If not set, the server does not return any group related access information.
  6: optional set<string> groups_to_return_permissions_for

  // Offset and count for pagination. The first `offset` datasets are skipped (after
  // matching filters) and at most `count` are returned. Not that this is not
  // transactional, if datasets get added or removed while paging through them, results
  // will be inconsistent
  7: optional i32 offset
  8: optional i32 count

  // Returns the total matched datasets. This is expected to be used with pagination
  // to return the total count.
  9: optional bool return_total
}

struct TGetDatasetsResult {
  1: required list<RecordService.TTable> datasets

  // If 'groups_to_return_permissions_for' is specified in the request, for each
  // dataset in 'datasets', the list of groups with some access to the dataset.
  // i.e. 'groups_with_access[i]' are the groups that have access to 'datasets[i]'
  3: optional list<set<string>> groups_with_access

  // For each dataset in `datasets`, true, if this user is admin on it.
  5: optional list<bool> is_admin

  // For each dataset in `datasets`, true, if it is a public dataset.
  7: optional list<bool> is_public

  // List of datasets that failed to load. The server returns as many of the fields
  // as possible, but some may be unset as they could not load.
  // This list is always disjoint with `datasets.
  2: optional list<RecordService.TTable> failed_datasets

  // Map of databases that failed to load to the error.
  4: optional map<string, RecordService.TRecordServiceException> failed_databases

  // Set if `return_total` was set in the request.
  6: optional i32 total_count
}

// This currently just contains the fields to make this compatible with hive.
struct TUdf {
  1: required string database
  2: required string fn_signature
  3: required string class_name

  // The list of resources required to run this UDF. This can be for example, the list
  // of jars that need to be added that are required for the UDF.
  4: optional list<string> resource_uris
}

struct TGetUdfsParams {
  // List of databases to return UDFs for. If not set, returns it for all databases.
  1: optional list<string> databases
}

struct TGetUdfsResult {
  1: list<TUdf> udfs
}

struct TAddRemovePartitionsParams {
  1: required bool add           // Otherwise remove
  2: optional list<RecordService.TPartition> partitions
}

struct TAddRemovePartitionsResult {
  // Number of partitions added or removed
  1: required i32 count
}

enum TListFilesOp {
  LIST,
  READ,
  WRITE,
}

struct TListFilesParams {
  1: required TListFilesOp op

  // Either the name of a dataset[db.table] or a fully qualified path
  2: optional string object

  // If set, continue the current list for this request. The other fields
  // are ignored in that case and the parameters from the initial request are used.
  3: optional binary next_key

  // User running the request
  4: optional string requesting_user

  // For underlying file systems that support multiple versions of the same file,
  // the version id to use.
  5: optional string version_id
}

struct TListFilesResult {
  // These can either be signed or paths, depending on the operation. For listing,
  // it is the paths, for the read/write ops, these are signed urls.
  1: optional list<string> files
  2: optional bool done
}

// Okera extensions to the RecordServicePlanner API
service OkeraRecordServicePlanner extends RecordService.RecordServicePlanner {
  // Returns the access permissions for tables.
  TGetAccessPermissionsResult GetAccessPermissions(1: TGetAccessPermissionsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns role provenance for a user
  TGetRoleProvenanceResult GetRoleProvenance(1: TGetRoleProvenanceParams params)
    throws(1:RecordService.TRecordServiceException ex);

  // Executes a ddl command against the server, returning the results (if it produces
  // results).
  list<string> ExecuteDDL(1:TExecDDLParams ddl)
      throws(1:RecordService.TRecordServiceException ex);

  TExecDDLResult ExecuteDDL2(1:TExecDDLParams ddl)
      throws(1:RecordService.TRecordServiceException ex);

  // This will register aliases for 'user'. When the 'user' access path, it will
  // resolve to 'table'. If view is non-empty, a view will created for the user and
  // whenever the user access 'path' or 'table', it will resolve to the view.
  string RegisterAlias(1:string user, 2:string table, 3:string path, 4:string view)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the authenticated user from the user's token.
  TGetAuthenticatedUserResult AuthenticatedUser(1:string token)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the datasets. This is similar to RecordServicePlanner.GetTables() but
  // version2, which matches more advanced usage patterns better.
  TGetDatasetsResult GetDatasets(1:TGetDatasetsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the UDFs that have been registered. Note that this does not include
  // builtins, only functions explicilty registered by the user.
  TGetUdfsResult GetUdfs(1:TGetUdfsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Adds or remove partitions in bulk
  TAddRemovePartitionsResult AddRemovePartitions(1:TAddRemovePartitionsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the list of files specified in the params. This provides a file system
  // like interface.
  TListFilesResult ListFiles(1:TListFilesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the catalog objects registered for a given path prefix
  TGetRegisteredObjectsResult GetRegisteredObjects(1: TGetRegisteredObjectsParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Creates the attributes
  TCreateAttributesResult CreateAttributes(1:TCreateAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the list of attributes for the given filter
  // If no filter specified, returns the first 25 attributes sorted alphabetically
  TGetAttributesResult GetAttributes(1: TGetAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns the count of total records for the given object type
  // If the count is greater than max allowed, an estimated count is returned
  TGetCountResult GetRecordCount(1: TGetCountParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Assigns attributes to objects. The object can be database/table/column
  TAssignAttributesResult AssignAttributes(1: TAssignAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Removes attribute values from objects. The object can be database/table/column
  TUnassignAttributesResult UnassignAttributes(1: TUnassignAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Deletes the list of attributes
  TDeleteAttributesResult DeleteAttributes(1: TDeleteAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Returns a list of unique attribute namespaces
  TGetAttributeNamespacesResult GetAttributeNamespaces(
      1: TGetAttributeNamespacesParams params)
      throws(1:RecordService.TRecordServiceException ex);

  // Idempotently sets attributes to objects
  TSetAttributesResult SetAttributes(1: TSetAttributesParams params)
      throws(1:RecordService.TRecordServiceException ex);
}
