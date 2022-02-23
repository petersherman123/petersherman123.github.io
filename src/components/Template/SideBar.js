import React from 'react';
import { Link } from 'react-router-dom';

import ContactIcons from '../Contact/ContactIcons';

const { PUBLIC_URL } = process.env; // set automatically from package.json:homepage

const SideBar = () => (
  <section id="sidebar">
    <section id="intro">
      <Link to="/" className="logo">
        <img src={`${PUBLIC_URL}/images/me.jpg`} alt="" />
      </Link>
      <header>
        <h2>Peter Sherman</h2>
        <p><a href="mailto:petersherman@g.harvard.edu">petersherman@g.harvard.edu</a></p>
      </header>
    </section>

    <section className="blurb">
      <h2>About</h2>
      <p>Hi, I&apos;m Peter.
        I am a postdoctoral fellow at Harvard University working in the <a href="https://chinaproject.harvard.edu/people/peter-sherman">Harvard China Project</a>.
        I also work on the basketball analytics staff for the <a href="https://www.nba.com/magic/">Orlando Magic</a>. In my spare time, I enjoy reading, playing chess and playing/watching basketball.
      </p>
      <ul className="actions">
        <li>
          {!window.location.pathname.includes('/resume') ? <Link to="/resume" className="button">Learn More</Link> : <Link to="/about" className="button">About Me</Link>}
        </li>
      </ul>
    </section>

    <section id="footer">
      <ContactIcons />
      <p className="copyright">&copy; Peter Sherman <Link to="/">https://petersherman123.github.io/</Link>.</p>
    </section>
  </section>
);

export default SideBar;
