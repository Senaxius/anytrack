#include "example_interfaces/srv/add_two_ints.hpp"
#include "rclcpp/rclcpp.hpp"

class test_server : public rclcpp::Node  // MODIFY NAME
{
   public:
    test_server() : Node("test_server")  // MODIFY NAME
    {
        server_ = this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_two_ints", std::bind(&test_server::callback_test_server, this, std::placeholders::_1, std::placeholders::_2));

        RCLCPP_INFO(this->get_logger(), "Started test server...");
    }

   private:
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;

    void callback_test_server(const example_interfaces::srv::AddTwoInts::Request::SharedPtr request, const example_interfaces::srv::AddTwoInts::Response::SharedPtr response){
        response->sum = request->a + request->b;
        RCLCPP_INFO(this->get_logger(), "%ld", response->sum);
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<test_server>();  // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}