import os
import wave
import streamlit as st


def hide_message(audio_file, secret_msg, output_file):
    wave_audio = wave.open(audio_file, mode='rb')
    frame_bytes = bytearray(list(wave_audio.readframes(wave_audio.getnframes())))
    secret_msg += int((len(frame_bytes) - (len(secret_msg) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in secret_msg])))

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit

    frame_modified = bytes(frame_bytes)

    with wave.open(output_file, 'wb') as fd:
        fd.setparams(wave_audio.getparams())
        fd.writeframes(frame_modified)

    wave_audio.close()


def extract_message(audio_file):
    wave_audio = wave.open(audio_file, mode='rb')
    frame_bytes = bytearray(list(wave_audio.readframes(wave_audio.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    message = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    parts = message.split("###", 2)
    if parts:
        return parts[0]
    return None


def main():
    st.title("Hide and Extract Secret Message in Audio Wave File")

    operation = st.sidebar.selectbox("Select Operation", ["Hide Message", "Extract Message"])

    if operation == "Hide Message":
        st.subheader("Hide Message")
        audio_file = st.file_uploader("Select an Audio File", type=["wav"])
        secret_msg = st.text_area("Enter your Secret Message")
        output_file = st.text_input("Your Output file path and name")

        if st.button("Hide Message"):
            if audio_file and secret_msg and output_file:
                try:
                    hide_message(audio_file, secret_msg, output_file)
                    st.success("Message hidden successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please fill in all fields.")

    elif operation == "Extract Message":
        st.subheader("Extract Message")
        extracted_audio = st.file_uploader("Select the Modified Audio File", type=["wav"])

        if st.button("Extract Message"):
            if extracted_audio:
                try:
                    extracted_msg = extract_message(extracted_audio)
                    if extracted_msg:
                        st.success(f"Extracted Message: {extracted_msg}")
                    else:
                        st.warning("No message found in the audio.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please upload an audio file.")


if __name__ == "_main_":
    main()
