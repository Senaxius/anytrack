#include "example_interfaces/msg/string.hpp"
#include "rclcpp/rclcpp.hpp"

class test_listener : public rclcpp::Node  // MODIFY NAME
{
   public:
    test_listener() : Node("test_publisher")  // MODIFY NAME
    {
        subscriber_ = this->create_subscription<example_interfaces::msg::String>("test_publisher", 10, 
            std::bind(&test_listener::callback_test_topic, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "cpp test_listener has been started...");
    }

   private:
    void callback_test_topic(const example_interfaces::msg::String::SharedPtr msg){
        RCLCPP_INFO(this->get_logger(), "%s", msg->data.c_str());
    }
    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<test_listener>();  // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}