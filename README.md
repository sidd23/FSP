# FileSharingProtocol

* An application level server-client model FileSharingProtocol with support for uploading and downloading files and indexed searching.

* Client has the ability to do the following:
** Know the files present on the server side in the designated shared folder.
** Download files from this shared folder.

* File Transfer incorporates MD5checksum hash to handle file transfer errors.


##Commands

### IndexGet flag (args)
* shortlist (flag):
 * Client wants to know the names of files with timestamps within a particular range
 * Command format: $-> IndexGet shortlist <startTimeStamp> <endTimeStamp>
 * example command: $-> IndexGet shortlist YYYY MM DD HH:MM:SS YYYY MM DD HH:MM:SS
 * Output: includes 'filename', 'size', 'timestamp' and 'type/permissions' of the files between the start and end time stamps
*longlist (flag):
 * client gets the entire listing of the shared folder/directory including 'name', 'size', 'timestamp' and 'type/permissions' of files
 * example command: $-> IndexGet longlist
 * Output: same as shortlist but with complete file listing

### FileHash flag (args)
* Client can check if any of the files in the shared folder on the server side have been changed. 
* verify (flag):
 * Checks for the specified file name provided as a command line argument on the server side and returns the 'MD5checksum' and the 'last modified timestamp'.
 * command format: $-> FileHash verify <filename>
 * Output: 'MD5checksum' and 'lastModifiedTimeStamp'
* checkall (flag):
 * Does the same as verify except that it does so for all files on the server side.
 * command: $-> FileHash checkall
 * Output: 'filename', 'MD5checksum' and 'lastModifiedTimeStamp' of all files in the shared directory

### FileDownload flag args
* Used to download files from the shared folder on the server side to our folder.
* flag can take value of either TCP or UDP.
* Command format: $-> FileDownload TCP/UDP <filename>
* Output: filename, filesize (in bytes), last modified timestamp and the MD5 hash of the requested file.
