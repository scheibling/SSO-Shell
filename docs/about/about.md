# About SSO Shell - Introduction
This whole project started after a month-long search for the right piece of software for handling SSH authentication. Working in a publically funded company, the more expensive pieces of software are not available without some great effort as to motivate the costs, and we're just beginning our journey into Linux (ironically as somewhat of a cost-saving measure) and don't have many techs that currently are able to handle those servers. I also wanted a piece of software I could use in a similar fashion with my homelab and smaller company.

# The requirements
Our requirements were quite basic to begin with:
- Should be able to run on any server with OpenSSH-Server installed
- Should be able to run on any OpenSSH-client
- Must be compatible with OpenID Connect (for compatibility with our MFA-system)
- Must include a somewhat flexible system for access control
- Must include facilities for logging issued certificates, locally and to a central server via syslog

Since nobody is immune to a little bit of scope creep, the following were later added to the wishlist:
- Should have an API (-documentation) for developers to integrate their own clients or other software like ansible
- Support for SAML, LDAP and Built-in authentication
- API and/or integration with SCIM for user account lifecycling

# The competitors
We have been looking for a piece of software that can do at least these things for a while now:
- Authenticate users with a short-lived SSH Certificate for authentication to servers
- Be able to assign permissions to users and/or user groups
- Be able to assign permissions to servers and/or server groups
- Self-hosted

## Teleport (https://goteleport.com)
- [x] Self-hosted
- [x] Authentication via SSH certificates
- [x] Short-lived SSH Certificates
- [x] Open Source (partially)
- [x] OpenID Connect (github for free tier, others only in the enterprise version)
- [x] GUI for management

Teleport was the software that started this hunt over again after a couple of months, seemingly a well maintained piece of software with enterprise support. The problem was the lack of features, mainly OIDC, in the free version. This is potentially not a downside for other use cases, since it also comes with support and maintenance, but it wasn't the right fit for our needs at the moment.

## Smallstep (https://smallstep.com) Single Sign-On SSH
- [x] Self-hosted
- [x] Authentication via SSH certificates
- [x] Short-lived SSH Certificates
- [x] Open Source (partially)
- [x] OpenID Connect
- [x] Graphical interface

This product was more or less exactly what we're looking for, but the pricing for more than one user/host was a bit too high for us at the moment. 