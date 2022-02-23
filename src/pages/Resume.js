import React from 'react';
import { Link } from 'react-router-dom';

import Main from '../layouts/Main';

const Resume = () => (
  <Main
    title="Resume"
    description="Peter Sherman's Resume. Harvard University PhD in Earth and Planetary Sciences."
  >
    <article className="post" id="resume">
      <header>
        <div className="title">
          <h2 data-testid="heading"><Link to="resume">Resume</Link></h2>
        </div>
      </header>
      <object data="/images/Peter_Sherman_CV.pdf" type="application/pdf" width="100%" height="800px">
        <p>Alternative text - include a link <a href="https://drive.google.com/file/d/1ofuQymRay3IZ-Z-ZjGsG-xLUmfdqDdyG/view?usp=sharing">to the PDF!</a></p>
      </object>

    </article>
  </Main>
);

export default Resume;
