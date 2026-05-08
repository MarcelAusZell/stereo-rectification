import Latex from "../../utils/diplay_latex";

export default function EpipolarConstraint() {
  const baseUrl = import.meta.env.BASE_URL;

  return (
    <section id="epipolar-constraint" className="scroll-mt-24">
      <h1 className="mb-4 text-3xl font-bold text-red-400">The Epipolar Constraint</h1>
      <h1 className="mb-4 text-md font-bold text-red-300 ">Notation and Setup</h1>

      Given two cameras with camera projections centers <Latex>{"C"}</Latex> and <Latex>{"C'\\;"}</Latex>
      a 3D world point <Latex>{"P \\in \\mathbb{R}^3"}</Latex> is projected
      onto their corresponding image planes as image points
      <ul>
        <li><Latex>{"\\tilde{p} = \\begin{pmatrix}x & y & 1 \\end{pmatrix}^\\top"}</Latex> and </li>
        <li><Latex>{"\\tilde{p}' = \\begin{pmatrix}x' & y' & 1 \\end{pmatrix}^\\top"}</Latex></li>
      </ul>
      Each image plane has a principal point, denoted by <Latex>{"(c_x,c_y), (c_x',c_y')"}</Latex>.
      It is the point where the optical axis intersects the image plane.
      Equivalently, it is the projection of the camera center onto its own image plane.
      The distance between the camera projection centers and the princple points is given by the focal length <Latex>{"f"}</Latex>.
      <img
        className="block w-[75%] mx-auto mb-5"
        src={`${baseUrl}images/epipolor_gemoetry.svg`}
      />

      <h1 className="mb-4 text-md font-bold text-red-300">The Epipolar Constraint</h1>

      For obtaining a measure of correspondence between the two projections of the world point <Latex>{"P"}</Latex> we have to derive the epipolar constraint.


      The two camera projection centers <Latex>{"C"}</Latex> and <Latex>{"C'"}</Latex>
      together with the world point <Latex>{"P"}</Latex> span a plane in <Latex>{"\\mathbb{R}^3"}</Latex>,
      the so called epipolar plane.

      Since the image points <Latex>{"p"}</Latex> and <Latex>{"p'"}</Latex>
      are projections of the same world point <Latex>{"P"}</Latex>,
      the corresponding viewing rays must lie in this plane.

      Let the coordinate system of the left camera be chosen as the world coordinate system, i.e.

      The relative pose between the two cameras (i.e. from left to right) is described by a rotation matrix <Latex>{"R \\in SO(3)"}</Latex> and a translation vector <Latex>{"t \\in \\mathbb{R}^3"}</Latex>.
      That means, as we choose the coordinate system of the left camera as the world coordinate system, its pose is given by

      <ul>
        <li><Latex>{"R_{W \\to L} = I"}</Latex></li>
        <li><Latex>{"t_{W \\to L} = (0,0,0)^\\top"}</Latex></li>
      </ul>

      Hence, the left camera defines the origin and orientation of the global coordinate frame.
      The pose of the right camera is then expressed relative to this reference frame by the (this time non-trivial) rotation <Latex>{"R"}</Latex> and translation <Latex>{"t"}</Latex>.

      <ul>
        <li><Latex>{"R_{W \\to R} = R"}</Latex></li>
        <li><Latex>{"t_{W \\to R} = t"}</Latex></li>
      </ul>



      <img
        className="block w-[75%] mx-auto"
        src={`${baseUrl}images/epipolar_geometry_rotation_translation.svg`}
      />
      So all in all, the translation vector <Latex>{"t"}</Latex> describes the displacement between the two camera centers and therefore points from the left camera center <Latex>{"C"}</Latex> to the right camera center <Latex>{"C'"}</Latex>.
      and the rotation matrix <Latex>{"R"}</Latex> describes the orientation of the right camera relative to the left camera giving us our first connection between those two camera systems:
      <br />
      A 3D point <Latex>{"P \\in \\mathbb{R}^3"}</Latex> expressed in the coordinate system of the left camera can be transformed into the coordinate system of the right camera via

      <Latex block>
        {"\\begin{align*} \
            P' &= RP + t   \\\\     \
            t \\times P' &= t\\times (RP + t)   && \\textcolor{lightgray}{\\left(\\texttt{\\small{Cross product from left}}\\right)} \\\\     \
            t \\times P' &= t\\times RP + \\underbrace{t \\times t}_{=0}  && \\textcolor{lightgray}{\\left(\\texttt{\\small{Distributivity of Cross product}}\\right)}  \\\\   \
            \\underbrace{P' \\cdot (t \\times P')}_{=0} &= P' \\cdot (t\\times RP)  && \\textcolor{lightgray}{\\left(\\texttt{\\small{Dot Product from left}}\\right)}   \\\\  \
            0 &= P' \\cdot (t\\times RP)  && \\textcolor{lightgray}{\\left(\\texttt{\\small{Dot Product from left}}\\right)}  \\\\   \
            0 &= P' \\cdot (\\underbrace{t_\\times R}_{:=E}P)  && \\textcolor{lightgray}{\\left(t_\\times = \\begin{bmatrix}0 & -t_z & t_y \\\\t_z & 0 & -t_x \\\\-t_y & t_x & 0\\end{bmatrix}\\right)}  \\\\   \
            0 &= P' \\cdot EP  && \\textcolor{lightgray}{\\left(\\texttt{\\small{Essential matrix }} E = t_\\times R\\right)}  \\\\   \
            0 &= P'^\\top EP  && \\textcolor{lightgray}{\\left(\\texttt{\\small{Epipolar constraint}} \\right)}  \\\\   \
        \\end{align*}\
        "}
      </Latex>
    </section>
  );
}
