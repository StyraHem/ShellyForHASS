import React, { Component } from 'react';
import { Container, Nav, Navbar, NavDropdown, NavItem } from 'react-bootstrap';
//import type { History, InitialEntry, Location, Path, To } from "history";
import {
  Link,
  useLocation
} from 'react-router-dom';
import Button from 'react-bootstrap/Button'

export default function ShellyNavbar({narrow}) {
  const loc = useLocation()
  const ToggleSidebar = () => {
    const ha = document.querySelector("home-assistant")?.shadowRoot;
    const ham = ha?.querySelector("home-assistant-main")?.shadowRoot;
    const ad = ham?.querySelector("app-drawer") as any
    ad.opened=true;
  }
  return <>
    <Navbar collapseOnSelect bg="primary" variant="dark">
      <Container>                
        { narrow ? 
          <NavItem onClick={ToggleSidebar} className="ha-sidebar">
            <p className="navbar-toggler-icon"></p>
          </NavItem>
          : null
        }
        <Navbar.Brand as={Link} to="/">ShellyForHass</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" >
          <Nav className="me-auto" activeKey={loc.pathname}>
            {/* <Nav.Link as={Link} to="/" eventKey="/">Devices</Nav.Link> */}
            <Nav.Link as={Link} to="/config" eventKey="/config">Config</Nav.Link>
            <Nav.Link as={Link} to="/settings" eventKey="/settings">Settings</Nav.Link>
            {/* <Nav.Link as={Link} to="/readme" eventKey="/readme">Readme</Nav.Link> */}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  </>
}