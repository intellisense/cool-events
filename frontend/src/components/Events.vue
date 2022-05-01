<template>
  <v-container>
    <v-card
      elevation="12"
      width="100%"
      class="mx-auto"
    >
      <v-card-text>
        <v-row>
          <v-col>
            <v-data-table
              :headers="headers"
              :items="events"
              :loading="eventsLoading"
              :server-items-length="eventsCount"
              :options.sync="options"
              class="elevation-1 mb-2"
              disable-sort
              loading-text="Loading... Please wait"
            >
              <template #top>
                <v-toolbar
                  flat
                >
                  <v-toolbar-title>{{ title }}</v-toolbar-title>
                  <v-spacer />
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="handleCreate"
                  >
                    New Event
                  </v-btn>
                </v-toolbar>
              </template>
              <template #[`item.start_date`]="{ item }">
                <span>{{ item.start_date | formatDateTime }}</span>
              </template>
              <template #[`item.end_date`]="{ item }">
                <span>{{ item.end_date | formatDateTime }}</span>
              </template>
              <template #[`item.participants_count`]="{ item }">
                <v-chip
                  color="primary"
                  text-color="white"
                  small
                  @click="handleEventParticipantsModalOpen(item)"
                >
                  <v-avatar left>
                    <v-icon small>
                      mdi-account-multiple
                    </v-icon>
                  </v-avatar>
                  {{ item.participants_count }}
                </v-chip>
              </template>
              <template #[`item.actions`]="{ item }">
                <template v-if="isHost(item)">
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        color="primary"
                        class="mr-2"
                        small
                        v-bind="attrs"
                        v-on="on"
                        @click="handleEdit(item)"
                      >
                        mdi-pencil
                      </v-icon>
                    </template>
                    <span>Edit event</span>
                  </v-tooltip>
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        color="error"
                        small
                        v-bind="attrs"
                        v-on="on"
                        @click="handleDelete(item)"
                      >
                        mdi-delete
                      </v-icon>
                    </template>
                    <span>Delete event</span>
                  </v-tooltip>
                </template>
                <template v-else-if="isParticipant(item)">
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        color="error"
                        v-bind="attrs"
                        v-on="on"
                        @click="leave(item)"
                      >
                        mdi-calendar-remove
                      </v-icon>
                    </template>
                    <span>Withdraw from event</span>
                  </v-tooltip>
                </template>
                <template v-else>
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        color="primary"
                        v-bind="attrs"
                        v-on="on"
                        @click="attend(item)"
                      >
                        mdi-calendar-check
                      </v-icon>
                    </template>
                    <span>Attend event</span>
                  </v-tooltip>
                </template>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-card-text>
      <CreateUpdateEventModal
        :event-id="activeEventId"
        :visible="showCreateUpdateEventModal"
        @close="handleCreateUpdateEventModalClose"
        @event-updated="handleUpdated"
        @event-created="handleCreated"
      />
      <ConfirmDialog
        :on-confirm="handleConfirm"
        :visible="showConfirmModal"
        :title="deleteEventConfirmDialogTitle"
        :message="deleteEventConfirmDialogMessage"
        @close="showConfirmModal=false"
      />
      <EventParticipantsModal
        :event="activeEvent"
        :visible="showEventParticipantsModal"
        @close="handleEventParticipantsModalClose"
      />
    </v-card>
  </v-container>
</template>

<script>
import eventsAPI from '@/api/events';
import { mapState } from 'vuex';
import ConfirmDialog from './ConfirmDialog';
import CreateUpdateEventModal from './CreateUpdateEventModal';
import EventParticipantsModal from './EventParticipantsModal';

const deleteEventConfirmDialogTitle = 'Delete Event';
const deleteEventConfirmDialogMessage = 'Are you sure you want to delete this event?';

export default {
  name: 'Events',
  components: {
    CreateUpdateEventModal,
    ConfirmDialog,
    EventParticipantsModal,
  },
  props: {
    username: {
      type: String,
      required: false,
      default: null,
    },
    title: {
      type: String,
      required: false,
      default: 'Events',
    },
  },
  data() {
    return {
      eventsCount: 0,
      options: {},
      headers: [
        { text: 'Title', value: 'title', align: 'start' },
        { text: 'Start Date', value: 'start_date', align: 'center' },
        { text: 'End Date', value: 'end_date', align: 'center' },
        { text: 'Host', value: 'owner', align: 'start' },
        {
          text: 'Participants', value: 'participants_count', align: 'center', filterable: false,
        },
        {
          text: 'Actions', value: 'actions', sortable: false, filterable: false,
        },
      ],
      events: [],
      eventsLoading: false,
      activeEvent: null,
      deleteEventId: null,
      showCreateUpdateEventModal: false,
      showConfirmModal: false,
      deleteEventConfirmDialogTitle,
      deleteEventConfirmDialogMessage,
      showEventParticipantsModal: false,
    };
  },
  computed: {
    ...mapState('auth', ['user']),
    activeEventId() {
      return this.activeEvent ? this.activeEvent.id : null;
    },
  },
  watch: {
    options() {
      this.loadEvents();
    },
  },
  mounted() {
    this.loadEvents();
  },
  methods: {
    loadEvents() {
      const params = {
        page_size: this.options.itemsPerPage,
        page: this.options.page,
      };
      if (this.username) {
        params.owner = this.username;
      }
      this.eventsLoading = true;
      eventsAPI.events(params).then(({ data }) => {
        this.events = data.results;
        this.eventsCount = data.count;
        this.eventsLoading = false;
      });
    },
    handleCreate() {
      this.showCreateUpdateEventModal = true;
    },
    handleEdit(event) {
      this.activeEvent = event;
      this.showCreateUpdateEventModal = true;
    },
    handleDelete(event) {
      this.deleteEventId = event.id;
      this.showConfirmModal = true;
      this.deleteEventConfirmDialogMessage = `Are you sure you want to delete event "${event.title}"?`;
    },
    handleConfirm() {
      if (this.deleteEventId) {
        eventsAPI.deleteEvent(this.deleteEventId).then(() => {
          this.events.splice(this.events.findIndex((e) => e.id === this.deleteEventId), 1);
          this.deleteEventId = null;
          this.showConfirmModal = false;
          this.deleteEventConfirmDialogMessage = deleteEventConfirmDialogMessage;
        });
      }
    },
    handleCreateUpdateEventModalClose() {
      this.showCreateUpdateEventModal = false;
      this.activeEvent = null;
    },
    handleUpdated(event) {
      this.$set(this.events, this.events.findIndex((e) => e.id === event.id), event);
    },
    handleCreated(event) {
      this.events.unshift(event);
      this.eventsCount += 1;
    },
    isHost(event) {
      return event.attending.status === 'host';
    },
    isParticipant(event) {
      return event.attending.status === 'participant';
    },
    attend(event) {
      eventsAPI.attendEvent(event.id).then(() => {
        this.refreshEvent(event);
      });
    },
    leave(event) {
      eventsAPI.leaveEvent(event.id, event.attending.id).then(() => {
        this.refreshEvent(event);
      });
    },
    refreshEvent(event) {
      eventsAPI.getEvent(event.id).then(({ data }) => {
        this.$set(this.events, this.events.findIndex((e) => e.id === event.id), data);
      });
    },
    handleEventParticipantsModalOpen(event) {
      this.activeEvent = event;
      this.showEventParticipantsModal = true;
    },
    handleEventParticipantsModalClose() {
      this.activeEvent = null;
      this.showEventParticipantsModal = false;
    },
  },
};
</script>
