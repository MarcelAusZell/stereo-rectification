import { useEffect, useRef } from "react"

export default function DisplayVideo({ source, title, width }) {
  const wrapperRef = useRef(null)
  const videoRef = useRef(null)

  useEffect(() => {
    const el = wrapperRef.current
    const video = videoRef.current
    if (!el || !video) return

    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          video.play().catch(() => {})
        } else {
          video.pause()
        }
      },
      { threshold: 0.25 } // start when 25% visible
    )

    io.observe(el)
    return () => io.disconnect()
  }, [])

  return (
    <div className="flex justify-center">
      <div ref={wrapperRef} style={width ? { width } : undefined}>
        <video
          ref={videoRef}
          muted
          loop
          playsInline
          preload="none"
          className="block w-full h-auto"
        >
          <source src={source} type="video/mp4" />
        </video>

        {title && (
          <div className="mt-2 text-sm font-bold text-center">
            {title}
          </div>
        )}
      </div>
    </div>
  )
}