<template>
    <v-alert
      v-if="getMessage"
      dense
      :color="getAlertType"
      dark>
      <v-row align="center">
        <v-col class="grow">
          <div v-for="value, key in getMessage" :key="key">
            <strong v-if="key != 'non_field_errors'">{{ key }}:</strong>
              <div v-for="item in value" :key=item>{{ item }}</div>
          </div>
        </v-col>

        <v-col class="shrink">
          <div class="text-center">
            <v-btn
              depressed
              fab
              x-small
              :color="getAlertType"
              dark
              @click="clearMessage"
            >
              <v-icon>mdi-close</v-icon>
          </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-alert>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Message',
  computed: mapGetters(['getAlertType', 'getMessage']),
  methods: {
    clearMessage() {
      this.$store.dispatch('alertClear');
    },
  },
};
</script>

<style scoped>
</style>
