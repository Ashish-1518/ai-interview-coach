/**
 * VoiceRecorder — browser speech recognition + timer for spoken interview answers.
 *
 * Uses Web Speech API (webkitSpeechRecognition / SpeechRecognition) for real-time
 * transcript generation and standard timer state for WPM and speaking duration.
 */
import { useEffect, useRef, useState } from 'react'

interface VoiceRecorderProps {
  onTranscriptUpdate: (transcript: string) => void
  onVoiceAnalyzed?: (durationSeconds: number) => void
  disabled?: boolean
}

export function VoiceRecorder({
  onTranscriptUpdate,
  onVoiceAnalyzed,
  disabled = false,
}: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [seconds, setSeconds] = useState(0)
  const [supported, setSupported] = useState(true)

  const recognitionRef = useRef<any>(null)
  const timerRef = useRef<any>(null)

  useEffect(() => {
    // Check browser speech recognition support
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) {
      setSupported(false)
    }
  }, [])

  function toggleRecording() {
    if (isRecording) {
      stopRecording()
    } else {
      startRecording()
    }
  }

  function startRecording() {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

    if (!SpeechRecognition) return

    try {
      const recognition = new SpeechRecognition()
      recognition.continuous = true
      recognition.interimResults = true
      recognition.lang = 'en-US'

      recognition.onresult = (event: any) => {
        let currentTranscript = ''
        for (let i = 0; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript + ' '
        }
        onTranscriptUpdate(currentTranscript.trim())
      }

      recognition.onerror = () => {
        stopRecording()
      }

      recognition.start()
      recognitionRef.current = recognition
      setIsRecording(true)
      setSeconds(0)

      timerRef.current = setInterval(() => {
        setSeconds((s) => s + 1)
      }, 1000)
    } catch {
      setIsRecording(false)
    }
  }

  function stopRecording() {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop()
      } catch {
        // Ignore
      }
    }
    if (timerRef.current) {
      clearInterval(timerRef.current)
    }
    setIsRecording(false)

    if (seconds > 0 && onVoiceAnalyzed) {
      onVoiceAnalyzed(seconds)
    }
  }

  if (!supported) {
    return (
      <div className="text-xs text-slate-400">
        🎙 Microphone speech-to-text supported in Chrome / Edge.
      </div>
    )
  }

  return (
    <div className="flex items-center gap-3">
      <button
        type="button"
        onClick={toggleRecording}
        disabled={disabled}
        className={`flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors ${
          isRecording
            ? 'animate-pulse bg-bad-500 text-white'
            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
        }`}
      >
        <span>{isRecording ? '🔴 Stop Recording' : '🎙 Speak Answer'}</span>
        {isRecording && <span className="font-mono">{seconds}s</span>}
      </button>
      {isRecording && (
        <span className="text-xs text-slate-500 animate-pulse">
          Listening to microphone...
        </span>
      )}
    </div>
  )
}
