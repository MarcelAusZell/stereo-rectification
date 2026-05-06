import Latex from "../../utils/diplay_latex";

export default function EpipolarGeometry() {
  return (
    <section id="epipolar-geometry" className="scroll-mt-24">
      <h1 className="mb-4 text-3xl font-bold text-red-400">Understanding Epipolar Geometry</h1>

      Given two cameras with camera projections centers <Latex>{"C"}</Latex> and <Latex>{"C'\\;"}</Latex>
      a 3D world point <Latex>{"P \\in \\mathbb{R}^3"}</Latex> is projected
      onto their corresponding image planes as a pixel point <Latex>{"p"}</Latex> and <Latex>{"p'\\;"}</Latex>
      respectively.
      Each image plane has a principal point, denoted by <Latex>{"(c_x,c_y), (c_x',c_y')"}</Latex>.
      It is the point where the optical axis intersects the image plane.
      Equivalently, it is the projection of the camera center onto its own image plane.
      The distance between the camera projection centers and the princple points is given by the focal length <Latex>{"f"}</Latex>.
      <img
        className="block w-[80%] mx-auto"
        src="/images/epipolor_gemoetry_unaligned_cameras.svg"
      />
      <img
        className="block w-[80%] mx-auto"
        src="/images/epipolor_gemoetry_aligned_cameras.svg"
      />


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