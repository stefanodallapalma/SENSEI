1) URL INFORMATION

Anita platform url: localhost:3000
Anita platform backend url: http://0.0.0.0:4000/

2) ISSUES
New endpoints: if the load dump endpoint contains a db_platform_updated = False, then execute these 4 endpoints to force the update of the db used for the anita gui

1) Update Products
- type: get
- endpoint: http://0.0.0.0:5000/v1/platform-update/products/
- result: true if the update has been successfully execuyted, false otherwise

2) Update Vendors
- type: get
- endpoint: http://0.0.0.0:5000/v1/platform-update/vendors/
- result: true if the update has been successfully execuyted, false otherwise

3) Update Pseudonym
- type: get
- endpoint: http://0.0.0.0:5000/v1/platform-update/pseudonym/
- result: true if the update has been successfully execuyted, false otherwise

4) Update Feedback
- type: get
- endpoint: http://0.0.0.0:5000/v1/platform-update/feedback/
- result: true if the update has been successfully execuyted, false otherwise

If you want to delete the entire platform database, then use the following endpoint

1) Delete all
- type: delete
- endpoint: http://0.0.0.0:5000/v1/platform-update/products/
- result: true if the update has been successfully execuyted, false otherwise