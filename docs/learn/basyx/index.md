# BaSyx

This page gives a quick, practical introduction to Asset Administration Shells (AAS) and the core BaSyx components you will encounter. In the BaSyx docs, these server-side building blocks are called **components**.

## AAS in one minute

An **Asset Administration Shell (AAS)** is the digital representation of an asset. It provides access to the information about that asset through a standard HTTP/REST interface. That information is organized into **Submodels**, which each cover a specific aspect (for example, identification, technical data, or documentation).

## The main BaSyx components (and what they do)

### AAS Environment

The **AAS Environment** is a convenience component that bundles three repositories into one service:

- **AAS Repository**: stores AAS instances and provides CRUD APIs for them.
- **Submodel Repository**: stores Submodel instances and provides CRUD APIs for them.
- **Concept Description Repository**: stores Concept Descriptions and provides CRUD APIs for them.

If you want a single backend endpoint that can store all core AAS data, start here.

### Registry services

Registries do not store the full AAS/Submodel payloads. Instead, they store **descriptors** that help clients locate where the full data lives and point to the network endpoints of AAS or Submodels.

- **AAS Registry**: registers and searches AAS descriptors (which also include Submodel descriptors).
- **Submodel Registry**: registers and searches Submodel descriptors.

Registries are the “phone book” for distributed AAS data.

### AAS Discovery Service

The **Discovery Service** helps clients find AAS entries using asset identifiers. In other words, it answers: *“Given an asset ID, which AAS belongs to it?”*

### AAS Web UI (optional)

The **AAS Web UI** is a client application to visualize and interact with AAS data. It is designed to work with AAS V3 registries, repositories, and the Discovery Service.

## How the pieces fit together

A typical setup looks like this:

1. **Store data**: Put AAS, Submodels, and Concept Descriptions into the AAS Environment (or into the three repositories if deployed separately).
2. **Register endpoints**: Register AAS and Submodel descriptors in the corresponding registries so clients can discover where the data is hosted.
3. **Discover by asset ID** (optional): Use the Discovery Service to map asset identifiers to AAS identifiers.
4. **Explore and test**: Use the AAS Web UI or your own client to browse and query.

## Minimal starting point

If you are new to AAS, start with:

- AAS Environment (for storage)
- AAS Registry + Submodel Registry (for discovery of endpoints)

Add Discovery Service and Web UI when you need asset-ID lookup and an interactive UI.
