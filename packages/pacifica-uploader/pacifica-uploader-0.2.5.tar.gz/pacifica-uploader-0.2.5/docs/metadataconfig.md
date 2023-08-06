# Uploader Metadata Configuration

The uploader configuration begins with an array of metadata objects.
The attributes of each object and how an uploader should manipulate
them are documented below. Much of the attributes define how a query
should be given to the policy server and how the user should be
presented with the results so they can make a choice.

Example Metadata Configuration Snippet:
```
{
  "destinationTable": "Transactions.submitter",
  "displayFormat": "{_id} - {first_name} {last_name}",
  "displayTitle": "Currently Logged On",
  "displayType": "logged_on",
  "metaID": "logon",
  "queryDependency": {},
  "queryFields": [
    "first_name",
    "last_name",
    "_id"
  ],
  "sourceTable": "users",
  "value": "",
  "valueField": "_id"
}
```

 * Destination Table - `destinationTable`

The destination table and column for the value to be put into. The
value is a string of the format `TABLE.COLUMN`.

 * Display Format - `displayFormat`

The formatted string to show the user an entry for data from the
`sourceTable`. This is uploader independent and uses string
formatting specific to Python (in this implementation) for rendering
the string.

 * Display Title - `displayTitle`

The title for the resulting data returned from the query.

 * Display Type - `displayType`

This is for the uploader to choose the values for. This may represent
a select drop down list, a radio button options or whatever the
uploader would like to present to the user.

 * Metadata ID - `metaID`

This is the unique ID for the metadata in the system. This should be
a unique string for all metadata objects for the entire configuration.

 * Query Dependencies - `queryDependency`

This is a hash containing the dependencies for the query and where to
find the values in the current metadata configuration. The hash is a
`column` to `metaID` mapping. These dependencies are passed as `where`
arguments to the policy query.

 * Query Fields - `queryFields`

This is a list of columns from the source field to pull in as part of
the query. These will be given to the `displayFormat` string to render
the entry for users to pick.

 * Source Table - `sourceTable`

The source table from which the query will be requesting data from.

 * Result Value - `value`

The value of the `valueField` column from the `sourceTable` to be put
into the `destinationTable` for the upload.

 * Value Field - `valueField`

The value field to be put into the table and column defined by
`destinationTable`.
