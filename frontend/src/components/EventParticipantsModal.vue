<template>
  <v-dialog
    v-model="show"
    scrollable
    class="mx-auto"
    max-width="500px"
  >
    <v-card v-if="event">
      <v-card-title>
        <span class="headline">{{ event.participants_count }} Event Participants</span>
      </v-card-title>

      <v-list two-line>
        <template v-for="(participant, index) in participantsList">
          <v-divider
            :key="index"
          />
          <v-list-item
            :key="participant.id"
          >
            <v-list-item-avatar color="cyan lighten-2">
              <v-icon dark>
                mdi-account-circle
              </v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title v-text="participant.username" />
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
      <div
        v-if="event.participants_count > pageSize"
        class="text-center"
      >
        <v-pagination
          v-model="page"
          :length="totalPages"
          total-visible="4"
          @input="getEventParticipants"
        />
      </div>

      <v-card-actions>
        <div class="flex-grow-1" />
        <v-btn
          color="blue-grey darken-1"
          text
          @click="show=false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import eventsAPI from '@/api/events';

export default {
  name: 'EventParticipantsModal',
  props: {
    visible: {
      type: Boolean,
      required: true,
      default: false,
    },
    event: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      page: 1,
      pageSize: 5,
      participants: null,
    };
  },
  computed: {
    show: {
      get() {
        return this.visible;
      },
      set(value) {
        if (!value) {
          this.$emit('close');
        }
      },
    },
    participantsList() {
      return this.participants ? this.participants : [];
    },
    participantsCount() {
      return this.event ? this.event.participants_count : 0;
    },
    totalPages() {
      return Math.ceil(this.participantsCount / this.pageSize);
    },
  },
  watch: {
    show(currVal, prevVal) {
      if (!currVal && prevVal) {
        this.resetModal();
      }

      if (currVal && !prevVal) {
        if (this.event.id) {
          this.getEventParticipants();
        }
      }
    },
  },
  methods: {
    getEventParticipants() {
      const params = {
        page_size: this.pageSize,
        page: this.page,
      };
      eventsAPI.getEventParticipants(this.event.id, params).then(({ data }) => {
        this.participants = data.results;
      });
    },
    resetModal() {
      this.participants = null;
      this.page = 1;
    },
  },
};
</script>
