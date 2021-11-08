import React, { Component } from 'react';
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import type { History, InitialEntry, Location, Path, To } from "history";
import { Link } from 'react-router-dom';
import {
  useLocation
} from 'react-router-dom';


export default function ShellyNavbar() {
  const loc = useLocation()
  return <>
    <Navbar expand="lg" collapseOnSelect bg="primary" variant="dark">
      <Container>
        <Navbar.Brand as={Link} to="/">ShellyForHass</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto" activeKey={loc.pathname}>
            <Nav.Link as={Link} to="/" eventKey="/">Devices</Nav.Link>
            <Nav.Link as={Link} to="/config" eventKey="/config">Config</Nav.Link>
            <Nav.Link as={Link} to="/settings" eventKey="/settings">Settings</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  </>
}