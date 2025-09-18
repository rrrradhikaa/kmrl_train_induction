import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // your backend URL

// Fitness Certificates
export const getFitnessCertificates = () =>
  axios.get(`${API_BASE_URL}/fitness_certificates`);

// Job Cards
export const getJobCards = () =>
  axios.get(`${API_BASE_URL}/job_cards`);

// Mileage Balancing
export const getMileageBalancing = () =>
  axios.get(`${API_BASE_URL}/mileage_balancing`);

// Branding Priorities
export const getBrandingPriorities = () =>
  axios.get(`${API_BASE_URL}/branding_priorities`);

// Cleaning Slots
export const getCleaningSlots = () =>
  axios.get(`${API_BASE_URL}/cleaning_slots`);

// Stabling Geometry
export const getStablingGeometry = () =>
  axios.get(`${API_BASE_URL}/stabling_geometry`);
