# Vaccination Demography Tracking Platform
The Vaccination Demography Tracking Platform is a web application designed to track vaccination data and demographic information using a NoSQL database powered by DataStax Cassandra. The backend of the platform is built with Django, utilizing the django_cassandra_engine for seamless integration with Cassandra.

## Features
* Vaccination Data Management: Capture, store, and manage vaccination data for different demographics.
* Demographic Information: Track demographic information such as age, gender, location, and vaccination status.
* Real-time Updates: Utilize DataStax Cassandra to provide real-time updates and scalable storage for large datasets.
* Assign Doctors: Each of the family can be assigned a family doctor.

## Technologies Used
* Django: Python-based web framework for building the backend of the application.
* django_cassandra_engine: Django database backend for Cassandra, enabling seamless integration with Django ORM.
* DataStax Cassandra: NoSQL distributed database for scalable and high-performance data storage.
* Python 3: Programming language used for backend development.
* HTML/CSS/JavaScript: Frontend technologies for building the user interface and client-side interactions.
* Bootstrap: Frontend framework for responsive and mobile-friendly design.

## Installation and Setup
Clone the Repository:
git clone https://github.com/geekynice/vaxTracker.git

## Install Dependencies:
pip install -r requirements.txt

## Configure Cassandra Database:
Install and configure DataStax Cassandra on your system.
Update the settings.py file with the Cassandra database configuration.

## Sync Database:
python manage.py syncdb

## Start the Development Server:
python manage.py runserver

## Access the Application:
Visit http://localhost:8000 in your web browser to access the application.

## Contributing
Contributions are welcome! Please open issues or pull requests for bug fixes, improvements, or new features.

## License
This project is licensed under the MIT License.

## Contact
For inquiries or support, don't hesitate to get in touch with me.