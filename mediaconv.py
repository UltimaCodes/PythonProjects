# Basic media converter that uses moviepy

from moviepy.editor import VideoFileClip
import os

def convert_media(input_file, output_format):
    try:
        # Get the filename without extension
        file_name, _ = os.path.splitext(input_file)
        # Set the output file name with the desired format
        output_file = f"{file_name}.{output_format}"
        
        if output_format.lower() in ["mp3"]:
            # Extract audio for MP3
            clip = VideoFileClip(input_file)
            clip.audio.write_audiofile(output_file)
            clip.close()
        else:
            # Convert video formats
            clip = VideoFileClip(input_file)
            clip.write_videofile(output_file)
            clip.close()

        print(f"Conversion successful! File saved as {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")

def main():
    print("Welcome to the General Media Converter!")
    while True:
        # Get input file from user
        input_file = input("\nEnter the path of the media file to convert: ")
        
        if not os.path.isfile(input_file):
            print("File not found! Please enter a valid file path.")
            continue
        
        print("\nChoose the output format:")
        print("1: MP4")
        print("2: MP3")
        print("3: AVI")
        print("4: MOV")
        print("5: MKV")
        print("6: Exit")
        
        choice = input("Enter your choice (1-6): ")
        format_mapping = {
            "1": "mp4",
            "2": "mp3",
            "3": "avi",
            "4": "mov",
            "5": "mkv"
        }
        
        if choice == "6":
            print("Goodbye!")
            break
        elif choice in format_mapping:
            output_format = format_mapping[choice]
            convert_media(input_file, output_format)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
