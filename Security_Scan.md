As part of the Code Analysis, 13 Vulnerabilities were identified, which were of the following severity : 
High – 4
Medium - 9

The Vulnerability types identified were – 
1. Path Traversal (High)
2. Origin Validation Error (Medium)
3. Debug  Mode Enabled (Medium)

Description of findings : 
1. Path Traversal - Unsanitized input from the HTTP request body flows into save, where it is used as a path. This will allow an attacker to write arbitrary files.
2. Origin Validation Error - CORS policy "*" might be too permissive. This allow malicious code on other domains to communicate with the application, 
which is a security risk.
3. Debug Mode Enabled - Running the application in debug mode is a security risk if the application is accessible by untrusted parties.


Analysis and Best Practices

Path Traversal
Details : 
A Directory Traversal attack (also known as path traversal) aims to access files and directories that are stored outside the intended folder. 
By manipulating files with "dot-dot-slash (../)" sequences and its variations, or by using absolute file paths, it may be possible to access arbitrary files and directories stored on file system, 
including application source code, configuration, and other critical system files.
Being able to access and manipulate an arbitrary path leads to vulnerabilities when a program is being run with privileges that the user providing the path should not have. 
A website with a path traversal vulnerability would allow users access to sensitive files on the server hosting it. CLI programs may also be vulnerable to path traversal if they are being ran with elevated privileges (such as with the setuid or setgid flags in Unix systems).

Directory Traversal vulnerabilities can be generally divided into two types:

• Information Disclosure: 
Allows the attacker to gain information about the folder structure or read the contents of sensitive files on the system.
st is a module for serving static files on web pages and contains a vulnerability of this type. In our example, we will serve files from the public route.
If an attacker requests the following URL from our server, it will in turn leak the sensitive private key of the root user.
curl http://localhost:8080/public/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/root/.ssh/id_rsa
Note %2e is the URL encoded version of . (dot).
• Writing arbitrary files: 
Allows the attacker to create or replace existing files. This type of vulnerability is also known as Zip-Slip.
One way to achieve this is by using a malicious zip archive that holds path traversal filenames. 
When each filename in the zip archive gets concatenated to the target extraction folder, without validation, the final path ends up outside of the target folder. 
If an executable or a configuration file is overwritten with a file containing malicious code, the problem can turn into an arbitrary code execution issue quite easily.

Origin Validation Error
Details
As a legacy of early web design and site limitations, most web applications default, for security reasons, to a "same origin policy". 
This means that browsers can only retrieve data from another site if the two sites share the same domain. 
In today's complex online environment, however, sites and applications often need to retrieve data from other domains. 
This is done under fairly limited conditions through an exception to the same origin policy known as "cross-origin resource sharing".
Developers may create definitions of trusted domains that are broader than absolutely necessary, inadvertently opening up wider access than intended. 
This weakness could result in data exposure or loss, or even allow an attacker to take over the site or application.

Best practices for prevention
• Avoid using wildcards for cross-origin resource sharing. Instead, define intended domains explicitly.
• Ensure that your site or app is well defended against cross-site scripting attacks (XSS), which could lead to takeover via an overly permissive 
cross-domain policy.
• Do not mix secure and insecure protocols when defining cross-domain policies.
• Consider defining a clear approved list to specify which domains will be given resource-level access; use this approved list to validate all domain access requests.
• Clearly define which methods (view, read, and update) are permitted for each resource and domain to avoid abuse.

Debug Mode Enabled
Details
When debugging, it may be necessary to report detailed information to a developer. However, if the debugging code is not disabled when the application is operating in a production environment, then this sensitive information may be exposed to attackers.