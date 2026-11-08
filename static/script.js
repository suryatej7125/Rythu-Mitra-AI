const recordBtn = document.getElementById("recordBtn");
const statusText = document.getElementById("status");

const resultCard = document.getElementById("result");
const questionText = document.getElementById("question");
const answerText = document.getElementById("answer");
const sourceText = document.getElementById("source");
const responseAudio = document.getElementById("responseAudio");

let mediaRecorder;
let audioChunks = [];
let isRecording = false;


// START OR STOP RECORDING
recordBtn.addEventListener("click", async () => {

    if (!isRecording) {
        await startRecording();
    } else {
        stopRecording();
    }

});


// START RECORDING
async function startRecording() {

    try {

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        audioChunks = [];

        let mimeType = "";

        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
            mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/mp4")) {
            mimeType = "audio/mp4";
        }

        mediaRecorder = mimeType
            ? new MediaRecorder(stream, { mimeType })
            : new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {

            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }

        };

        mediaRecorder.onstop = async () => {

            const audioBlob = new Blob(audioChunks, {
                type: mediaRecorder.mimeType
            });

            stream.getTracks().forEach(track => track.stop());

            await sendAudioToServer(audioBlob);

        };

        mediaRecorder.start();

        isRecording = true;

        recordBtn.textContent = "⏹ Stop Recording";
        recordBtn.classList.add("recording");

        statusText.textContent = "🎙️ Listening... Speak your farming question.";

        resultCard.classList.add("hidden");

    } catch (error) {

        console.error("Microphone error:", error);

        statusText.textContent =
            "Microphone access denied. Please allow microphone permission.";

    }

}


// STOP RECORDING
function stopRecording() {

    if (mediaRecorder && mediaRecorder.state !== "inactive") {

        mediaRecorder.stop();

        isRecording = false;

        recordBtn.textContent = "🎤 Start Speaking";
        recordBtn.classList.remove("recording");

        statusText.textContent =
            "⏳ Processing your question... Please wait.";

    }

}


// SEND AUDIO TO PYTHON BACKEND
async function sendAudioToServer(audioBlob) {

    try {

        const formData = new FormData();

        formData.append(
            "audio",
            audioBlob,
            "farmer_question.webm"
        );

        statusText.textContent =
            "🌱 Understanding your farming question...";

        const response = await fetch("/api/ask", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        // DISPLAY QUESTION AND ANSWER

        questionText.textContent = data.question;
        answerText.textContent = data.answer;
        sourceText.textContent = data.source || "No source information available.";

        resultCard.classList.remove("hidden");

        // PLAY GENERATED TELUGU AUDIO

        responseAudio.src = data.audio_url;

        statusText.textContent =
            "✅ Your answer is ready!";

        recordBtn.disabled = false;

        // Automatically play the response
        try {
            await responseAudio.play();
        } catch (playError) {
            console.log("Automatic playback blocked. Use the audio player.");
        }

    } catch (error) {

        console.error("Application error:", error);

        statusText.textContent =
            "❌ " + error.message;

    }

}
// TEXT QUESTION FEATURE

const textQuestion = document.getElementById("textQuestion");
const askTextBtn = document.getElementById("askTextBtn");


askTextBtn.addEventListener("click", async () => {

    const question = textQuestion.value.trim();

    if (!question) {
        statusText.textContent = "Please enter your farming question.";
        textQuestion.focus();
        return;
    }

    try {

        askTextBtn.disabled = true;

        statusText.textContent =
            "🌱 Rythu Mitra is thinking...";

        resultCard.classList.add("hidden");

        const response = await fetch("/api/ask-text", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        // DISPLAY QUESTION AND ANSWER

        questionText.textContent = data.question;
        answerText.textContent = data.answer;
        sourceText.textContent = data.source || "No source information available.";

        resultCard.classList.remove("hidden");

        // PLAY TELUGU VOICE RESPONSE

        responseAudio.src = data.audio_url;

        statusText.textContent =
            "✅ Your answer is ready!";

        try {
            await responseAudio.play();
        } catch (playError) {
            console.log("Use the audio player to hear the answer.");
        }

    } catch (error) {

        console.error("Text question error:", error);

        statusText.textContent = "❌ " + error.message;

    } finally {

        askTextBtn.disabled = false;

    }

});