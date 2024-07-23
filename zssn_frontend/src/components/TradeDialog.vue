<template>
  <v-card>
    <v-card-title>
      <v-row>
        <v-col class="d-flex align-center">
          <div>Trade Requests</div>
        </v-col>
        <v-col class="d-flex justify-end">
          <v-btn v-if="!showCreateForm" color="primary" @click="openCreateForm">
            <v-icon left>mdi-plus</v-icon>
            Create
          </v-btn>
          <v-btn color="red" dark class="ml-1" @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-row v-if="!showCreateForm">
          <v-col cols="12" md="12">
            <h3 class="mb-4">Pending Trade Requests</h3>
            <v-row>
              <v-col v-for="item in pendingRequests" :key="item.id" cols="12" md="6">
                <v-card>
                  <v-card-title>
                    <v-container>
                      <v-row>
                        <v-col cols="12" md="5">
                          <div>
                            <div>Requester ID: {{ item.requesterId }}</div>
                            <div>Requester Name:<br> {{ item.requesterName }}</div>
                          </div>
                        </v-col>
                        <v-col cols="12" md="2" class="d-flex justify-center align-center">
                          <v-icon>mdi-swap-horizontal</v-icon>
                        </v-col>
                        <v-col cols="12" md="5">
                          <div class="text-right">
                            <div>Receiver ID: {{ item.receiverId }}</div>
                            <div>Receiver Name:<br> {{ item.receiverName }}</div>
                          </div>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-title>
                  <v-card-subtitle>
                    <div><strong>Requester Items:</strong></div>
                    <v-simple-table>
                      <thead>
                        <tr>
                          <th class="text-left">Item</th>
                          <th class="text-left">Quantity</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(quantity, itemName) in item.requesterItems" :key="itemName">
                          <td>{{ itemName }}</td>
                          <td>{{ quantity }}</td>
                        </tr>
                      </tbody>
                    </v-simple-table>
                    <div><strong>Receiver Items:</strong></div>
                    <v-simple-table>
                      <thead>
                        <tr>
                          <th class="text-left">Item</th>
                          <th class="text-left">Quantity</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(quantity, itemName) in item.receiverItems" :key="itemName">
                          <td>{{ itemName }}</td>
                          <td>{{ quantity }}</td>
                        </tr>
                      </tbody>
                    </v-simple-table>
                  </v-card-subtitle>
                  <v-card-actions>
                    <v-container>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-btn v-if="selectedSurvivor.id !== item.requesterId" color="green"
                            @click="handleTradeRequest(item, 'Approved')" block dark>
                            <v-icon left>mdi-check</v-icon>
                            Approve
                          </v-btn>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-btn color="red" @click="handleTradeRequest(item, 'Cancel')" block dark>
                            <v-icon left>mdi-close</v-icon>
                            {{ selectedSurvivor.id === item.requesterId ? 'Cancel' : 'Deny' }}
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
            <v-pagination class="mt-2" v-model="pendingRequestCurrentPage" :length="pendingRequestTotalPages"
              @input="onPageChange"></v-pagination>
          </v-col>
        </v-row>
        <v-row v-if="showCreateForm">
          <v-col cols="12">
            <v-card>
              <v-card-title>Create New Trade Offer</v-card-title>
              <v-card-subtitle>
                <v-container>
                  <v-row>
                    <v-col cols="12" md="6">
                      <h3 class="mb-6 mt-6">Requester: {{ selectedSurvivor.name }}</h3>
                      <v-simple-table>
                        <thead>
                          <tr>
                            <th class="text-left header-item"></th>
                            <th class="text-left header-quantity"></th>
                            <th class="text-left header-available"></th>
                            <th class="text-center header-action"></th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in selectedSurvivor.inventory" :key="item.id">
                            <td>{{ item.item_name }}</td>
                            <td>{{ item.item_quantity }}</td>
                            <td>{{ calculateAvailable('requester', item) }}</td>
                            <td class="text-center">
                              <v-btn icon color="blue" @click="increaseItemQuantity('requester', item.item_name)"
                                :disabled="calculateAvailable('requester', item) <= 0">
                                <v-icon>mdi-plus</v-icon>
                              </v-btn>
                              {{ tradeOffer.requesterItems[item.item_name] || 0 }}
                              <v-btn icon color="red" @click="decreaseItemQuantity('requester', item.item_name)"
                                :disabled="(tradeOffer.requesterItems[item.item_name] || 0) <= 0">
                                <v-icon>mdi-minus</v-icon>
                              </v-btn>
                            </td>
                          </tr>
                        </tbody>
                      </v-simple-table>
                      <hr>
                      <div class="text-center">Total Points: {{ requesterTotalPoints }}</div>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-autocomplete v-model="selectedReceiverId" :items="otherSurvivors" item-text="name"
                      item-value="id" label="Select Receiver"
                      @update:search-input="fetchSurvivorsSearch" />
                      <v-simple-table v-if="selectedReceiver && selectedReceiver.inventory">
                        <thead>
                          <tr>
                            <th class="text-left header-item trim-text"></th>
                            <th class="text-left header-quantity trim-text"></th>
                            <th class="text-left header-available trim-text"></th>
                            <th class="text-center header-action"></th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in selectedReceiver.inventory" :key="item.id">
                            <td class="trim-text">{{ item.item_name }}</td>
                            <td class="trim-text">{{ item.item_quantity }}</td>
                            <td>{{ calculateAvailable('receiver', item) }}</td>
                            <td class="text-center">
                              <v-btn icon color="blue" @click="increaseItemQuantity('receiver', item.item_name)"
                                :disabled="calculateAvailable('receiver', item) <= 0">
                                <v-icon>mdi-plus</v-icon>
                              </v-btn>
                              {{ tradeOffer.receiverItems[item.item_name] || 0 }}
                              <v-btn icon color="red" @click="decreaseItemQuantity('receiver', item.item_name)"
                                :disabled="(tradeOffer.receiverItems[item.item_name] || 0) <= 0">
                                <v-icon>mdi-minus</v-icon>
                              </v-btn>
                            </td>
                          </tr>
                        </tbody>
                      </v-simple-table>
                      <hr v-if="selectedReceiver && selectedReceiver.inventory">
                      <div v-if="selectedReceiver && selectedReceiver.inventory" class="text-center">Total Points: {{
            receiverTotalPoints }}</div>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-subtitle>
              <v-card-actions class="center-actions">
                <v-btn color="blue" dark @click="submitTradeOffer" :disabled="!pointsAreEqual">Submit</v-btn>
                <v-btn color="red" dark @click="hideCreateForm">Cancel</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    selectedSurvivor: Object,
    survivors: Array
  },
  data() {
    return {
      showCreateForm: false,
      itemPrices: {
        water: 4,
        food: 3,
        medication: 2,
        ammunition: 1
      },
      search: '',
      tradeOffer: {
        requesterId: null,
        receiverId: null,
        requesterItems: {},
        receiverItems: {},
        totalTradePoints: 0,
        status: "Pending"
      },
      otherSurvivors: [],
      selectedReceiver: null,
      selectedReceiverId: null,
      pendingRequests: [],
      pendingRequestCurrentPage: 1,
      pendingRequestPerPage: 4,
      pendingRequestTotalPages: 1

    };
  },
  watch: {
    selectedReceiverId(newId) {
      this.selectedReceiver = this.otherSurvivors.find(survivor => survivor.id === newId) || null;
      this.tradeOffer.receiverItems = {};
    },
  },
  computed: {
    requesterTotalPoints() {
      return this.calculateTotalPoints(this.tradeOffer.requesterItems);
    },
    receiverTotalPoints() {
      return this.calculateTotalPoints(this.tradeOffer.receiverItems);
    },
    pointsAreEqual() {
      return this.requesterTotalPoints === this.receiverTotalPoints && this.requesterTotalPoints !== 0;
    },
  },
  mounted() {
    this.fetchPendingRequests(1, this.selectedSurvivor.id);
  },
  methods: {
    onPageChange(page) {
      this.pendingRequestCurrentPage = page;
      this.fetchPendingRequests(page, this.selectedSurvivor.id);
    },
    closeDialog() {
      this.$emit('close-trade-dialog');
    },
    openCreateForm() {
      this.showCreateForm = true;
      this.pendingRequestCurrentPage = 1; 
    },
    hideCreateForm() {
      this.showCreateForm = false;
      this.tradeOffer.receiverItems = {};
      this.tradeOffer.requesterItems = {};
      this.selectedReceiver = null;
      this.selectedReceiverId = null;
      this.search = '';
      this.otherSurvivors = [];
      this.pendingRequestCurrentPage = 1;

    },
    async fetchPendingRequests(page = 1, survivorId = '') {
      if (survivorId === null || survivorId === undefined) {
        survivorId = '';
      }
      axios.get(`http://localhost:8000/api/trade_offers/?page=${page}&survivorId=${survivorId}`)
        .then(response => {
          let responseData = response.data.results;
          this.pendingRequestCurrentPage = page;
          this.pendingRequestTotalPages = Math.ceil(response.data.count / this.pendingRequestPerPage);
          
          responseData.forEach(request => {
            ['requesterItems', 'receiverItems'].forEach(key => {
              if (request[key] && typeof request[key] === 'object') {
                Object.keys(this.itemPrices).forEach(itemName => {
                  if (!Object.prototype.hasOwnProperty.call(request[key], itemName)) {
                    request[key][itemName] = 0;
                  }
                });

                const orderedItems = {};
                Object.keys(this.itemPrices).forEach(itemName => {
                  orderedItems[itemName] = request[key][itemName];
                });

                request[key] = orderedItems;
              } else {
                console.error(`Invalid request.${key} format:`, request[key]);
              }
            });
          });

          this.pendingRequests = responseData;

        })
        .catch(error => {
          console.error("There was an error fetching the pending trade requests:", error);
        });
    },
    increaseItemQuantity(type, itemName) {
      const availableQuantity = this.calculateAvailableByName(type, itemName);
      if (availableQuantity > 0) {
        if (!this.tradeOffer[`${type}Items`][itemName]) {
          this.$set(this.tradeOffer[`${type}Items`], itemName, 1);
        } else {
          this.tradeOffer[`${type}Items`][itemName]++;
        }
      }
    },
    decreaseItemQuantity(type, itemName) {
      if (this.tradeOffer[`${type}Items`][itemName] > 1) {
        this.tradeOffer[`${type}Items`][itemName]--;
      } else {
        this.$delete(this.tradeOffer[`${type}Items`], itemName);
      }
    },
    calculateTotalPoints(items) {
      let total = 0;
      for (const [itemName, quantity] of Object.entries(items)) {
        total += this.itemPrices[itemName] * quantity;
      }
      return total;
    },
    calculateAvailable(type, item) {
      const blocked = item.item_quantity_blocked || 0;
      const requested = type === 'requester' ? this.tradeOffer.requesterItems[item.item_name] || 0 : 0;
      const received = type === 'receiver' ? this.tradeOffer.receiverItems[item.item_name] || 0 : 0;
      return item.item_quantity - (blocked + requested + received);
    },
    calculateAvailableByName(type, itemName) {
      if (type === 'requester') {
        const item = this.selectedSurvivor.inventory.find(i => i.item_name === itemName);
        if (item) {
          return this.calculateAvailable('requester', item);
        }
      } else if (type === 'receiver') {
        const item = this.selectedReceiver.inventory.find(i => i.item_name === itemName);
        if (item) {
          return this.calculateAvailable('receiver', item);
        }
      }
    },
    async handleTradeRequest(tradeRequest, tradeStatus) {

      if (tradeStatus && tradeRequest && tradeRequest.id) {
        axios.patch(`http://localhost:8000/api/trade_offers/${tradeRequest.id}/`, {
          status: tradeStatus,
        })
        .then(() => {
          this.fetchPendingRequests(1 ,this.selectedSurvivor.id);
        })
        .catch(error => {
          console.error('Error approving request', error);
        });}
    },
    submitTradeOffer() {
      if (this.pointsAreEqual) {
        this.tradeOffer.requesterId = this.selectedSurvivor.id;
        this.tradeOffer.receiverId = this.selectedReceiver.id;
        this.tradeOffer.status = 'Pending';
        this.tradeOffer.totalPrice = this.requesterTotalPoints;
        
        axios.post('http://localhost:8000/api/trade_offers/', 
          this.tradeOffer
        )
          .then(() => {
            this.hideCreateForm();
            this.fetchPendingRequests(1, this.selectedSurvivor.id);
          }).catch(error => {
            console.error(error);
          });
      } else {
        console.error('Trade points mismatch');
      }
    },
    fetchSurvivorsSearch(search) {
      this.fetchSurvivors(1, search);
    },
    async fetchSurvivors(page = 1, search = '') {
      search = search === null ? '' : search;
      axios.get(`http://localhost:8000/api/survivors/?page=${page}&search=${search}`)
        .then(response => {
          this.otherSurvivors = response.data.results.filter(survivor => survivor.id !== this.selectedSurvivor.id);
        })
        .catch(error => {
          console.error("There was an error fetching the survivors:", error);
        });
    },
  }
};
</script>

<style scoped>
.trim-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.center-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.header-item::after {
  content: "Item";
}

.header-quantity::after {
  content: "Quantity";
}

.header-available::after {
  content: "Available";
}

.header-action::after {
  content: "Action";
}

/* Mobile styles */
@media (max-width: 600px) {
  .header-item::after {
    content: "Item";
  }

  .header-quantity::after {
    content: "Q";
  }

  .header-available::after {
    content: "A";
  }

  .header-action::after {
    content: "A";
  }
}
</style>