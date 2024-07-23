<template>
  <v-app>
    <v-container>
      <v-toolbar color="primary" dark>
        <v-toolbar-title class="text-center w-100">Zombie Survival Social Network</v-toolbar-title>
      </v-toolbar>
      <v-tabs v-model="tab" background-color="primary" dark>
        <v-tab>Survivors</v-tab>
        <v-tab>Map</v-tab>
        <v-tab>Create New Survivor</v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab" touchless>

        <v-tab-item>
          <v-container class="grey lighten-5">
            <v-row v-if="!tradeDialog">
              <v-col cols="12">
                <v-text-field v-model="search" label="Search by Name" @input="fetchSurvivors(1, search)"
                  prepend-icon="mdi-magnify" clearable></v-text-field>
              </v-col>
            </v-row>
            <v-row v-if="!tradeDialog">
              <v-col v-for="survivor in survivors" :key="survivor.id" cols="12" sm="6" md="4">
                <v-card>
                  <v-list-item>
                    <v-list-item-avatar>
                      <img src="../assets/user.png" alt="User Avatar" />
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title>{{
        formatName(survivor.name)
      }}</v-list-item-title>
                      <v-list-item-subtitle>{{ survivor.age }} -
                        {{ survivor.gender }}</v-list-item-subtitle>
                      <v-list-item-subtitle>Location: {{ survivor.last_location_latitude }},
                        {{
        survivor.last_location_longitude
      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-card-text>
                    <v-divider></v-divider>
                    <v-simple-table dense>
                      <thead>
                        <tr>
                          <th class="text-left">Item Name</th>
                          <th class="text-left">Quantity</th>
                          <th class="text-left">Blocked</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in survivor.inventory" :key="item.id">
                          <td>{{ formatName(item.item_name) }}</td>
                          <td>{{ item.item_quantity }}</td>
                          <td>{{ item.item_quantity_blocked }}</td>
                        </tr>
                      </tbody>
                    </v-simple-table>
                    <v-divider></v-divider>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="12">
                          <v-btn color="red" block dark @click="openReportDialog(survivor)">Report a Person</v-btn>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" sm="12">
                          <v-btn color="green" block dark @click="openTradeDialog(survivor)">Trade Requests</v-btn>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" sm="12">
                          <v-btn color="blue" block dark @click="openUpdateDialog(survivor)">Update Location</v-btn>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row v-if="!tradeDialog">
              <v-col cols="12">
                <v-pagination v-model="currentPage" :length="totalPages" @input="fetchSurvivorsPagination"
                  :total-visible="7"></v-pagination>
              </v-col>
            </v-row>
            <v-row v-if="tradeDialog">
              <v-col cols="12">
                <TradeDialog :selectedSurvivor="selectedSurvivor" :survivors="survivors"
                  @close-trade-dialog="closeTradeDialog" />
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>

        <v-tab-item>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="search" label="Search by Name" @input="fetchSurvivors(1, search)"
                  prepend-icon="mdi-magnify" clearable></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <div ref="mapContainer" class="map-container">
                  <l-map v-if="mapKey" :key="mapKey" :zoom="3" :center="[48.20499918, 16.370498518]"
                    :options="{ tap: false, scrollWheelZoom: false }">
                    <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"></l-tile-layer>
                    <l-marker v-for="survivor in survivors" :key="survivor.id" :lat-lng="[
        survivor.last_location_latitude,
        survivor.last_location_longitude,
      ]" :icon="customIcon">
                      <l-tooltip permanent>{{ survivor.name }}</l-tooltip>
                    </l-marker>
                  </l-map>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-pagination v-model="currentPage" :length="totalPages" @input="fetchSurvivorsPagination"
                  :total-visible="7"></v-pagination>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>

        <v-tab-item>
          <v-container>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-row>
                <v-col cols="12" sm="12">
                  <v-text-field v-model="newSurvivor.name" :rules="[rules.required, rules.max255]" label="Name"
                    required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.age" :rules="[rules.required, rules.age]" label="Age" type="number"
                    required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select v-model="newSurvivor.gender" :items="['Male', 'Female', 'Other']" :rules="[rules.required]"
                    label="Gender" required></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.last_location_latitude" :rules="[rules.required, rules.latitude]"
                    label="Latitude" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.last_location_longitude" :rules="[rules.required, rules.longitude]"
                    label="Longitude" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.inventory[0].item_quantity"
                    :rules="[rules.required, rules.inventory]" label="Water" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.inventory[1].item_quantity"
                    :rules="[rules.required, rules.inventory]" label="Food" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.inventory[2].item_quantity"
                    :rules="[rules.required, rules.inventory]" label="Medication" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="newSurvivor.inventory[3].item_quantity"
                    :rules="[rules.required, rules.inventory]" label="Ammunition" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-btn :disabled="!valid" @click="createSurvivor">Submit</v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-container>
        </v-tab-item>
      </v-tabs-items>

      <v-dialog v-model="updateDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">Update Location</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="updateLocationValid">
              <v-text-field v-model="updatedLatitude" label="Latitude" :rules="[rules.required, rules.latitude]"
                required type="number"></v-text-field>
              <v-text-field v-model="updatedLongitude" label="Longitude" :rules="[rules.required, rules.longitude]"
                required type="number"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closeUpdateDialog">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="submitLocation">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      
      <v-dialog v-model="reportDialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Report Infected Survivors</span>
          </v-card-title>
          <v-card-text>
            <v-autocomplete v-model="selectedInfectedSurvivor" :items="formattedSurvivors" item-text="name"
              item-value="id" label="Select Infected Survivor" chips clearable solo hide-details
              @update:search-input="fetchSurvivorsSearch" />
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closeReportDialog">Cancel</v-btn>
            <v-btn color="red darken-1" text @click="reportInfected">Report</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">{{ dialogTitle }}</v-card-title>
          <v-card-text>{{ dialogMessage }}</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </v-app>
</template>

<script>
import axios from "axios";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import TradeDialog from './TradeDialog.vue';


const customIcon = new L.Icon({
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"), 
  iconSize: [25, 41], 
  iconAnchor: [12, 41], 
  popupAnchor: [1, -34], 
  shadowSize: [41, 41], 
});

export default {
  components: {
    TradeDialog
  },
  data() {
    return {
      mapKey: 1,
      infectedSearchHolder: "",
      infectedCurrentPageHolder: 1,
      search: "",
      currentPage: 1,
      pageSize: 12,
      totalPages: 1,
      customIcon,
      tab: 0,
      tradeDialog: false,
      updateDialog: false,
      updateLocationValid: false,
      updatedLatitude: "",
      updatedLongitude: "",
      valid: false,
      reportDialog: false,
      selectedInfectedSurvivor: "",
      dialog: false,
      dialogTitle: "",
      dialogMessage: "",
      selectedSurvivor: {},
      newSurvivor: {
        name: "",
        age: "",
        gender: "",
        last_location_latitude: "",
        last_location_longitude: "",
        reported_by: [],
        inventory: [
          {
            item_name: "water",
            item_quantity: "",
            item_quantity_blocked: 0,
            is_locked: false
          },
          {
            item_name: "food",
            item_quantity: "",
            item_quantity_blocked: 0,
            is_locked: false
          },
          {
            item_name: "medication",
            item_quantity: "",
            item_quantity_blocked: 0,
            is_locked: false
          },
          {
            item_name: "ammunition",
            item_quantity: "",
            item_quantity_blocked: 0,
            is_locked: false
          }
        ]
      },
      survivors: [],
      rules: {
        required: (value) => !!value || "Required.",
        max255: (value) =>
          (value && value.length <= 255) || "Max 255 characters.",
        age: (value) =>
          (value >= 1 && value <= 150) || "Age must be between 1 and 150.",
        latitude: (value) =>
          (value >= -90 && value <= 90) ||
          "Latitude must be between -90 and 90 degrees.",
        longitude: (value) =>
          (value >= -180 && value <= 180) ||
          "Longitude must be between -180 and 180 degrees.",
        number: (value) => !isNaN(value) || "Must be a number.",
        inventory: (value) =>
          (!isNaN(value) && value >= 0) || "Must be a non-negative number.",
      },
    };
  },
  computed: {
    formattedSurvivors() {
      return this.survivors.map((survivor) => ({
        ...survivor,
        name: this.formatName(survivor.name),
      }));
    },
  },
  methods: {
    fetchSurvivorsPagination(newPage) {
      this.fetchSurvivors(newPage, this.search);
    },
    fetchSurvivorsSearch(search) {
      this.fetchSurvivors(1, search);
    },
    createMap() {
      this.$nextTick(() => {
        if (this.$refs.map) {
          this.$refs.map.mapObject.invalidateSize();
        }
      });
    },
    destroyMap() {
      if (this.$refs.map) {
        this.$refs.map.mapObject.remove();
      }
    },
    handleResize() {
      this.destroyMap();
      this.mapKey += 1;
      setTimeout(() => {
        this.createMap();
      }, 500);
    },
    showAlert(title, message) {
      this.dialogTitle = title;
      this.dialogMessage = message;
      this.dialog = true;
    },
    async createSurvivor() {
      if (this.$refs.form.validate()) {
      
        axios.post(
          "http://localhost:8000/api/survivors/",
          this.newSurvivor
        )
        .then(() => {
          this.fetchSurvivors();
          this.newSurvivor = {
            name: "",
            age: "",
            gender: "",
            last_location_latitude: "",
            last_location_longitude: "",
            inventory: [
              {
                item_name: "water",
                item_quantity: "",
                item_quantity_blocked: 0,
                is_locked: false
              },
              {
                item_name: "food",
                item_quantity: "",
                item_quantity_blocked: 0,
                is_locked: false
              },
              {
                item_name: "medication",
                item_quantity: "",
                item_quantity_blocked: 0,
                is_locked: false
              },
              {
                item_name: "ammunition",
                item_quantity: "",
                item_quantity_blocked: 0,
                is_locked: false
              }
            ]
          };
          
          this.$refs.form.reset();
          this.showAlert(
            "Successful Operation",
            "Survivor created successfully!"
          );
        })
        .catch(error => {
          console.error("Error creating survivor:", error);
          this.showAlert("Error", this.trimErrorMessage(error.request.responseText));
        });
      }
    },
    async fetchSurvivors(page = 1, search = '') {
      search = search === null ? '' : search;
      axios.get(`http://localhost:8000/api/survivors/?page=${page}&search=${search}`)
        .then(response => {
          this.survivors = response.data.results; 
          this.currentPage = page;
          this.totalPages = Math.ceil(response.data.count / this.pageSize);
        })
        .catch(error => {
          console.error("There was an error fetching the survivors:", error);
          this.showAlert("Error", this.trimErrorMessage(error.request.responseText));
        });
    },
    openTradeDialog(survivor) {
      this.selectedSurvivor = survivor;
      this.tradeDialog = true;
    },
    closeTradeDialog() {
      this.tradeDialog = false;
      this.selectedSurvivor = {};
      this.fetchSurvivors(this.currentPage, this.search);
    },
    openReportDialog(survivor) {
      this.reportDialog = true;
      this.selectedSurvivor = survivor;
      this.infectedSearchHolder = this.search;
      this.infectedCurrentPageHolder = this.currentPage;
    },
    closeReportDialog() {
      this.reportDialog = false;
      this.selectedSurvivor = {};
      this.selectedInfectedSurvivor = "";
      this.search = this.infectedSearchHolder;
      this.currentPage = this.infectedCurrentPageHolder;
      this.fetchSurvivors(this.currentPage, this.search);
      this.infectedSearchHolder = "";
      this.infectedCurrentPageHolder = 1;
    },
    openUpdateDialog(survivor) {
      this.selectedSurvivor = survivor;
      this.updatedLatitude = survivor.last_location_latitude;
      this.updatedLongitude = survivor.last_location_longitude;
      this.updateDialog = true;
    },
    closeUpdateDialog() {
      this.updateDialog = false;
      this.selectedSurvivor = {};
      this.updatedLatitude = "";
      this.updatedLongitude = "";
    },
    trimErrorMessage(errorMessage) {
      return errorMessage.slice(2, -2);
    },
    async submitLocation() {
      if (this.$refs.form.validate()) {
        const payload = {
          id: this.selectedSurvivor.id,
          last_location_latitude: this.updatedLatitude,
          last_location_longitude: this.updatedLongitude,
        };
        axios.patch(
          `http://localhost:8000/api/survivors/${this.selectedSurvivor.id}/`,
          payload
        )
        .then(() => {
          this.fetchSurvivors(this.currentPage, this.search);
          this.showAlert(
            "Location Updated",
            "Survivor location has been updated."
          );

          this.closeUpdateDialog();
        })
        .catch(error => {
          console.error("Error updating location:", error);
          this.showAlert("Error", this.trimErrorMessage(error.request.responseText));
        });        
      }
    },
    async reportInfected() {
      axios.patch(
        `http://localhost:8000/api/survivors/${this.selectedInfectedSurvivor}/`,
        {
          id: this.selectedInfectedSurvivor,
          reported_by: [this.selectedSurvivor.id]
        }
      )
      .then(() => {
        this.closeReportDialog();
        this.fetchSurvivors(this.currentPage, this.search);
        this.showAlert(
          "Report Infected",
          "You have reported an infected person."
        );
      })
      .catch(error => {
        this.closeReportDialog();
        console.error("Error reporting infected survivor:", error);
        this.showAlert("Error", this.trimErrorMessage(error.request.responseText));
      });


    },
    formatName(name) {
      return name
        .split(" ")
        .map(
          (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        )
        .join(" ");
    },
  }, watch: {
    tab(newTab) {
      this.search = "";
      this.currentPage = 1;
      this.fetchSurvivors();
      if (newTab === 1) {
        setTimeout(() => {
          this.handleResize(), 500
        });
      }
    },
  },
  mounted() {
    this.fetchSurvivors();
    this.createMap();
    window.addEventListener('resize', this.handleResize);

  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    this.destroyMap();
  },
};
</script>
<style scoped>
.map-container {
  height: 100vh;
  width: 100%;
  max-height: 500px;
}
</style>
<style>
@import "~leaflet/dist/leaflet.css";
</style>
