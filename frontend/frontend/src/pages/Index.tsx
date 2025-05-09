import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { Footer } from "@/components/layout/Footer";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-col md:flex-row flex-1">
        <Sidebar />

        <div className="flex-1 flex items-center justify-center bg-whatsapp-lightBg p-4">
          <div className="text-center max-w-md">
            <h2 className="text-2xl font-bold text-whatsapp-darkGreen mb-4">Welcome to WhatsApp Management</h2>
            <p className="text-gray-600">
              Select a conversation from the sidebar to view messages or search for specific conversations.
            </p>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Index;