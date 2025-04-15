<script lang="ts">
import Button from '$lib/components/ui/button/button.svelte';
import { onMount } from 'svelte';

let counts = {
  burgers: 0,
  fries: 0,
  drinks: 0
};

let orderHistory: { burgers: number; fries: number; drinks: number; message: string; }[] = [];
const HISTORY_KEY = 'OrderHistory';

onMount(() => {
  const history = localStorage.getItem(HISTORY_KEY);
  if (history) {
    orderHistory = JSON.parse(history);
    if (orderHistory.length > 0) {
      // Set counts to the total of all orders
      counts = orderHistory.reduce(
        (acc, order) => ({
          burgers: acc.burgers + order.burgers,
          fries: acc.fries + order.fries,
          drinks: acc.drinks + order.drinks
        }),
        { burgers: 0, fries: 0, drinks: 0 }
      );
    }
  }
});

function updateHistory() {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(orderHistory));
}

let chatMessage = '';

function runMessage() {
  // You can handle the chat message here (e.g., send to backend, show in UI, etc.)
  alert(`Message sent: ${chatMessage}`);

  // update history
  updateHistory();
}
</script>

<div class="px-32 flex flex-col items-center">

    <!-- Total counts -->
    <div class="flex gap-8 justify-center items-center mt-16">
        {#each Object.entries(counts) as [item, value]}
            <div class="bg-white shadow-lg rounded-xl p-8 flex flex-col items-center justify-between">
                <h2 class="text-2xl font-bold capitalize">Total # of {item}</h2>
                <div class="text-5xl mt-8">{value}</div>
            </div>
        {/each}
    </div>

    <!-- Chat input box -->
    <div class="w-full flex justify-center mt-16">
        <div class="flex gap-2 w-full max-w-xl items-center">
        <input
            class="flex-1 border border-gray-300 rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            type="text"
            bind:value={chatMessage}
            placeholder="Drive thru message"
        />
        <Button size="lg" variant="default" on:click={runMessage}>Run</Button>
        </div>
    </div>

    <!-- Order History Section -->
    <div class="w-full flex flex-col items-center mt-16">
      <h2 class="text-2xl font-bold mb-4">Order History</h2>
      {#if orderHistory.length === 0}
        <div class="text-gray-500">No orders yet.</div>
      {:else}
        <div class="w-full max-w-2xl">
          <div class="grid grid-cols-5 gap-4 font-semibold border-b pb-2 mb-2">
            <div>Order #</div>
            <div>Burgers</div>
            <div>Fries</div>
            <div>Drinks</div>
            <div>Message</div>
          </div>
          {#each orderHistory as order, i}
            <div class="grid grid-cols-5 gap-4 py-2 border-b items-center">
              <div>{i + 1}</div>
              <div>{order.burgers}</div>
              <div>{order.fries}</div>
              <div>{order.drinks}</div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
</div>
