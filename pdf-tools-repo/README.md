# PDF Manipulation Tools Website

## Overview

This project provides a web-based application for manipulating PDF files directly in the browser. It allows users to perform various operations on PDF files, including compression, conversion to Word, conversion to images, and conversion to Excel formats. The website is built using modern web technologies and libraries to ensure a seamless and efficient user experience.

## Technologies Used

- **HTML**: For structuring the web page.
- **CSS**: For styling the web page. Bootstrap is used to make the design responsive and visually appealing.
- **JavaScript**: For handling user interactions and implementing the core functionalities of PDF manipulation.
- **Bootstrap**: A front-end framework used for designing responsive and mobile-first websites.
- **pdf-lib**: A JavaScript library for manipulating PDF files, including tasks such as compression, merging, and splitting.
- **pdf2docx**: A library for converting PDF files to Word documents.
- **pdf2pic**: A library for converting PDF files to images.
- **xlsx-populate**: A library for creating and modifying Excel files.

## Architecture

The website's architecture is straightforward, consisting of a front-end built with HTML, CSS, and JavaScript. The front-end includes an HTML layout with elements for uploading PDF files, selecting conversion options, displaying results, and buttons for initiating actions. CSS, with the help of Bootstrap, styles these elements to make the website user-friendly and visually appealing. JavaScript, leveraging various libraries, handles user interactions and implements the functionalities for each PDF manipulation tool.

## Project Structure

- `index.html`: The main entry point of the website. It contains the layout for uploading PDF files, selecting manipulation options, and displaying results. Ensure `styles.css` is linked within the `<head>` section of `index.html`. Verify `main.js` is correctly referenced before the closing `</body>` tag in `index.html` with the `defer` attribute for proper scripting behavior.
- `styles.css`: Styles the elements defined in `index.html` to enhance the visual appeal and user experience of the website.
- `main.js`: Contains the logic for handling user interactions, such as file uploads and button clicks. It uses the libraries mentioned above to implement the functionalities for manipulating PDF files.

## Setting Up the Project Locally

To run this project locally, you need to have Node.js installed on your machine. Follow these steps to set up the project:

1. Ensure Node.js is installed by running `node --version` in your terminal. If Node.js is not installed, download and install it from [the official Node.js website](https://nodejs.org/).

2. Clone the repository to your local machine or download the source code.

3. Navigate to the project directory in your terminal.

4. To serve the `index.html` file, you can use a simple HTTP server. If you have Python installed, you can quickly start a server with the following command:
   - For Python 2.x: `python -m SimpleHTTPServer`
   - For Python 3.x: `python -m http.server`
   
   Alternatively, if you prefer using Node.js, you can install `http-server` by running `npm install -g http-server` and then start the server in your project directory by running `http-server`.

5. Open your browser and go to `http://localhost:8000` (or the port indicated by your HTTP server) to view the application.

## Running and Testing the Project

After setting up the project locally, you can test the PDF manipulation functionalities by uploading a PDF file and selecting the desired manipulation option. The website will process the file and provide feedback, such as progress indicators or status messages, during the file processing. Error handling is implemented to ensure users are informed if an operation fails or if an unsupported action is attempted.

For a more detailed understanding of how each file and functionality works, refer to the comments and documentation within the `index.html`, `styles.css`, and `main.js` files.

## Additional Information

This project is designed to demonstrate the capabilities of web technologies in manipulating PDF files directly in the browser. It is a proof of concept and may require additional security and functionality enhancements for production use.

Thank you for exploring the PDF Manipulation Tools website project!
```