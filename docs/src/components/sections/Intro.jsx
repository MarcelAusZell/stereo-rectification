import Latex from "../../utils/diplay_latex";
import CodeBlock from "../../utils/display_code";


export default function Intro() {
  return (
    <section id="introduction" className="scroll-mt-24">
      <h1 className="mb-4 text-3xl font-bold">Introduction</h1>
      <Latex>
        {"\\text{Attention}(\\mathbf{Q},\\mathbf{K},\\mathbf{V}) = " +
          "\\text{softmax}\\left(" +
          "\\frac{\\mathbf{QK}^\\top}{\\sqrt{d_k}}" +
          "\\right)\\mathbf{V}"}
      </Latex>
      <Latex block>
        {"\\text{Attention}(\\mathbf{Q},\\mathbf{K},\\mathbf{V}) = " +
          "\\text{softmax}\\left(" +
          "\\frac{\\mathbf{QK}^\\top}{\\sqrt{d_k}}" +
          "\\right)\\mathbf{V}"}
      </Latex>

      <CodeBlock
        width="100%"
        language="python"
        code={`print("test")
input_video = cv2.VideoCapture("./inputs.mp4")
frame_ok, frame = input_video.read()`} />
    </section>
  );
}