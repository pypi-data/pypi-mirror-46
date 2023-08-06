# Uploader Expectations and Application Flows

This section describes how an end-user of Pacifica Python Uploader is expected
to interact with the modules, classes and methods above, and, by extension,
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) and
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) servers.

Keywords for the API
```
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).
```
### Uploader Program Flow

1. The uploader program MUST construct a new instance of the
   `pacifica.uploader.metadata.MetaUpdate` class. The new instance of the
   `pacifica.uploader.metadata.MetaUpdate` class MAY be associated with zero or more of
   instances of the `pacifica.uploader.metadata.MetaObj` class. The
   `pacifica.uploader.metadata.MetaObj.value` field MAY be `None`. The new instance of
   the `pacifica.uploader.metadata.MetaUpdate` class MUST NOT be associated with any
   instances of the `pacifica.uploader.metadata.FileObj` class.

2. To determine completeness, the new instance of the
   `pacifica.uploader.metadata.MetaUpdate` class SHOULD be validated using the
   `pacifica.uploader.metadata.MetaData.is_valid()` method (inherited by the
   `pacifica.uploader.metadata.MetaUpdate` sub-class). Then, the uploader program MUST
   call the `pacifica.uploader.metadata.PolicyQuery.PolicyQuery.valid_metadata()` method.
   The new instance of the `pacifica.uploader.metadata.MetaUpdate` class MUST be valid
   prior to bundling.

3. The uploader program MUST dereference the
   `pacifica.uploader.metadata.MetaObj.displayType` field to determine the mode of
   selection for the `pacifica.uploader.metadata.MetaObj.value` field. The value of the
   `pacifica.uploader.metadata.MetaObj.displayType` field is uploader-program-specific,
   i.e., the value MUST be defined by the uploader program.

4. The uploader program MUST assign a non-`None` value to each
   `pacifica.uploader.metadata.MetaData.query_results` field by calling the
   `pacifica.uploader.metadata.MetaUpdate.query_results()` method. The
   `pacifica.uploader.metadata.MetaData.query_results` field is a `list`.

5. The value of the `pacifica.uploader.metadata.MetaData.query_results` field MUST be
   rendered according to the uploader-program-specific definition that is
   interpreted from the value of the `pacifica.uploader.metadata.MetaObj.displayFormat`
   field, e.g., in the Python programming language, by calling the `str.format`
   method or by leveraging a template engine, such as
   [Cheetah](https://pypi.python.org/pypi/Cheetah) or
   [Jinja2](https://pypi.python.org/pypi/Jinja2).

6. The uploader program MAY call the
   `pacifica.uploader.metadata.MetaUpdate.query_results()` method for instances of the
   `pacifica.uploader.metadata.MetaObj` class whose `value` field is non-`None`.

7. The uploader program MUST handle all instances `pacifica.uploader.metadata.MetaUpdate`
   class, regardless of validity, i.e., the uploader program MUST NOT reject an
   instance of the `pacifica.uploader.metadata.MetaUpdate` class under any circumstances,
   e.g., if there are unsatisfied dependencies between instances of the
   `pacifica.uploader.metadata.MetaData` class.

8. When the uploader program is ready for a given
   `pacifica.uploader.metadata.MetaObj.value` field to be selected, the uploader program
   MUST assign to the `pacifica.uploader.metadata.MetaObj.value` field the value of the
   `pacifica.uploader.metadata.MetaObj.valueField` field, and then call the
   `pacifica.uploader.metadata.MetaObj.update_parents()` method. The effect of this
   operation is to update the `pacifica.uploader.metadata.MetaObj.value` fields of
   associated and dependent instances of the `pacifica.uploader.metadata.MetaObj` class.
   After modification, the new state of the instance of the
   `pacifica.uploader.metadata.MetaUpdate.MetaUpdate` class SHOULD be displayed to the
   end-user, as previously discussed.

9. The uploader program MUST verify that
   `pacifica.uploader.metadata.MetaUpdate.MetaUpdate.is_valid() == True`. If the instance
   of the `pacifica.uploader.metadata.MetaUpdate.MetaUpdate` class is not valid, then the
   uploader program MUST repeat the instructions in the paragraph 8.

10. The uploader program MUST call the
    `pacifica.uploader.metadata.PolicyQuery.PolicyQueryData.valid_metadata()` method to
    validate the instance of the `pacifica.uploader.metadata.MetaUpdate.MetaUpdate` class
    prior to upload. This prevents the uploader program from uploading metadata
    that is invalid with respect to the policy of the
    [Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) server.

11. When the uploader program is ready to bundle the data, the uploader program
    MUST construct a `list` of objects, representing the fields of the
    corresponding instance of the `tar.TarInfo` class. Each object MUST export a
    `fileobj` field whose value implements the file protocol, i.e., exports a
    `read()` method.

12. The uploader program MUST construct a new instance of the
    `pacifica.uploader.bundler.Bundler` class using the instances of the
    `pacifica.uploader.metadata.MetaUpdate.MetaUpdate` and `tar.TarInfo` classes, as
    previously stated in paragraph 11. Then, the uploader program MUST construct
    a file-like object that can be written to in binary mode, and then call the
    `pacifica.uploader.bundler.Bundler.stream()` method.

13. The uploader program MUST construct a new instance of the
    `pacifica.uploader.Uploader.Uploader` class. Then, the uploader program MUST
    construct a file-like object that can be read in binary mode, and then call
    the `pacifica.uploader.bundler.Bundler.upload()` method.

14. Finally, the uploader program MUST verify the result of the ingest by
    calling the `pacifica.uploader.Uploader.Uploader.getstate()` method. If an
    ingest-related error occurs, then the uploader program MAY repeat the ingest
    operation.
