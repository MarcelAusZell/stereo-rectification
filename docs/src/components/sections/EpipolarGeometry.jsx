import Latex from "../../utils/diplay_latex";

export default function EpipolarGeometry() {
  return (
    <section id="epipolar-geometry" className="scroll-mt-24">
      <h1 className="mb-4 text-3xl font-bold">Epipolar Geometry</h1>
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
    </section>
  );
}