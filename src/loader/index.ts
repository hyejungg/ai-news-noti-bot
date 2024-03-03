// import mongoose from "mongoose";
// import config from "../config";
// import Site from "../model/Site";

// const connectDB = async () => {
//     try {
//         await mongoose.connect(config.mongoDbUri);

//         mongoose.set("autoCreate", true);

//         console.log(`Mongoose Connected ...`);

//         Site.createCollection().then(function (collection) {
//             console.log("Site Collection is created!");
//         });
//     } catch (err: any) {
//         console.error(err.message);
//         process.exit(1);
//     }
// };

// export default connectDB;
