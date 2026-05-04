import { useEffect, useRef, useState } from "react"
import hljs from "highlight.js/lib/core"
import python from "highlight.js/lib/languages/python"
import javascript from "highlight.js/lib/languages/javascript"
import "highlight.js/styles/vs.css"

hljs.registerLanguage("python", python)
hljs.registerLanguage("javascript", javascript)

export default function CodeBlock({
  code,
  language = "javascript",
  width,
}) {
  const codeRef = useRef(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (codeRef.current) {
      hljs.highlightElement(codeRef.current)
    }
  }, [code])

  const resolvedWidth =
    typeof width === "number" ? `${width}px` : width

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch { }
  }

  return (
    <div className="flex justify-center my-4">
      <div
        className="relative"
        style={resolvedWidth ? { width: resolvedWidth } : undefined}
      >
        <button
          onClick={handleCopy}
          className="absolute bottom-2 right-0 flex items-center justify-center text-xs text-neutral/30 px-3 overflow-hidden rounded-t-xl border-tr-none font-bold pt-1 cursor-pointer"        >
          {copied ? "Copied" : "Copy"}
        </button>

        <pre className="overflow-auto border-3 border-base-300  rounded-md bg-base-200">
          <code ref={codeRef} className={`language-${language}`}>
            {code}
          </code>
        </pre>
      </div>
    </div>
  )
}