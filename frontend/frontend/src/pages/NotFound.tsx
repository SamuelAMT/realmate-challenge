
import { useEffect } from "react";
import { useLocation, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-whatsapp-lightBg">
        <div className="text-center max-w-md p-6 bg-white rounded-lg shadow-md">
          <h1 className="text-4xl font-bold text-whatsapp-darkGreen mb-4">404</h1>
          <p className="text-xl text-gray-600 mb-6">Oops! Conversation not found</p>
          <Button asChild>
            <Link to="/" className="flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Return to Conversations
            </Link>
          </Button>
        </div>
      </div>
  );
};

export default NotFound;
