# Flask Cafe Application

This is a Python Flask application for managing information about cafes. Users can view cafes, add new cafes, edit
existing cafes, and more.

## Setup

To run this application locally, follow these steps:

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/jakubswi/Cofe-and-Wiifi-Website.git
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    - Set `google_API_KEY` environment variable to your Google API key.
    - Set `secret_key` environment variable for Flask secret key.

5. Run the application:

    ```bash
    python app.py
    ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

- **Main Page**: The main page displays a list of all cafes stored in the database. Users can view details of each cafe.
- **View Cafe Details**: Clicking on a cafe's name will display its details, including name, location, map URL, image
  URL, availability of sockets, toilets, WiFi, ability to take calls, number of seats, and coffee price.
- **Add New Cafe**: Users can add a new cafe by navigating to the `/add-new-post` route. They need to provide all
  required information in the form provided.
- **Edit Cafe**: Existing cafes can be edited by navigating to the `/<id>/edit-post` route, where `<id>` is the ID of
  the cafe to be edited. Users can modify the details of the cafe using the form provided.

## Dependencies

- Flask
- Flask-Bootstrap5
- Flask-SQLAlchemy
- Flask-WTF

## Database

This application uses SQLite as its database. The database file `cafes.db` will be created in the project directory upon
running the application for the first time.

## Credits

This application was created by Jakub Świdłowski.

## License

This project is licensed under the [MIT License](LICENSE).
