import session from './session';

export default {
  events(params) {
    return session.get('/events/', { params: { ...params } });
  },
  createEvent(payload) {
    return session.post('/events/', payload);
  },
  updateEvent(eventID, payload) {
    return session.put(`/events/${eventID}/`, payload);
  },
  getEvent(eventID) {
    return session.get(`/events/${eventID}/`);
  },
  deleteEvent(eventID) {
    return session.delete(`/events/${eventID}/`);
  },
  attendEvent(eventID) {
    return session.post(`/events/${eventID}/participants/`);
  },
  leaveEvent(eventID, participantID) {
    return session.delete(`/events/${eventID}/participants/${participantID}/`);
  },
  getEventParticipants(eventID, params) {
    return session.get(`/events/${eventID}/participants/`, { params: { ...params } });
  },
};
