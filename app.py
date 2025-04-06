from flask import Flask, request, Response
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/api/convert', methods=['POST'])
def convert_to_black_and_white():
    # Check if an image file is present in the request
    if 'image' not in request.files:
        return {"error": "No image file provided"}, 400

    try:
        img_file = request.files['image']

        # Basic check for file extension (optional but good practice)
        # filename = img_file.filename
        # if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg')):
        #     return {"error": "Invalid file type. Please upload PNG or JPG."}, 400

        img = Image.open(img_file.stream)
        bw_img = img.convert('L')  # Convert the image to grayscale ('L' mode)
        
        img_byte_arr = io.BytesIO()
        bw_img.save(img_byte_arr, format='PNG') # Save as PNG
        img_byte_arr.seek(0) # Rewind the byte stream to the beginning
        
        return Response(
            img_byte_arr.getvalue(),
            mimetype='image/png' # Set correct MIME type for PNG
        )
    except Exception as e:
        # Log the error for debugging on the server
        print(f"Error processing image: {e}") 
        return {"error": "Failed to process image"}, 500 # Internal Server Error

# This line is generally NOT needed for Vercel deployment, 
# Vercel handles debug mode via environment variables if necessary.
# app.debug = True 

# This block is only for LOCAL testing, Vercel won't run it.
if __name__ == '__main__':
    # Use 0.0.0.0 to be accessible on your network
    # Port 5000 is common for Flask, but 5050 is fine too.
    app.run(debug=True, host='0.0.0.0', port=5050) 