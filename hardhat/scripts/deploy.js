const hre = require("hardhat");

async function main() {
  
  const Oracle = await hre.ethers.getContractFactory("oracle");
  const oracle= await Oracle.deploy();
  await oracle.deployed();

  const Consumer = await hre.ethers.getContractFactory("ATestnetConsumer");
  const consumer= await Consumer.deploy();
  await consumer.deployed();

  console.log("Consumer deployed to", consumer.address)  
  console.log("Oracle deployed to", oracle.address)

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});